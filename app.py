# ============================================================
# AI ATS Resume Optimizer
# pip install streamlit openai pdfplumber fpdf2 Pillow
# Run: streamlit run app.py
# ============================================================

import streamlit as st
import pdfplumber
import openai
import io
import re
from fpdf import FPDF

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI ATS Resume Optimizer",
    page_icon="📄",
    layout="wide",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main-header {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }

    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    .step-card {
        background: linear-gradient(135deg, #f8faff 0%, #eef2ff 100%);
        border: 1px solid #c7d2fe;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }

    .step-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: #6366f1;
        text-transform: uppercase;
        margin-bottom: 0.1rem;
    }

    .step-title {
        font-size: 0.95rem;
        font-weight: 500;
        color: #1e1b4b;
    }

    .info-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        border-radius: 0 8px 8px 0;
        padding: 0.85rem 1rem;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #78350f;
    }

    .success-box {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        border-radius: 0 8px 8px 0;
        padding: 0.85rem 1rem;
        margin: 1rem 0;
        font-size: 0.88rem;
        color: #14532d;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.8rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5, #4338ca);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transform: translateY(-1px);
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669, #047857) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
        margin-top: 0.5rem;
    }

    .stDownloadButton > button:hover {
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stFileUploader"] {
        border: 2px dashed #a5b4fc;
        border-radius: 10px;
        padding: 0.5rem;
        background: #f5f3ff;
    }

    .sidebar-key-box {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 0.4rem;
    }

    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Sidebar – API Key
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Your key is never stored. It is used only for this session."
    )
    st.markdown('<p class="sidebar-key-box">🔒 Your key is used only for this request and is not stored or logged.</p>', unsafe_allow_html=True)

    st.markdown("---")
    model_choice = st.selectbox(
        "Model",
        options=["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"],
        index=0,
        help="gpt-4o-mini offers the best speed/cost balance."
    )

    st.markdown("---")
    st.markdown("### 📋 How it works")
    steps = [
        ("01", "Upload your resume PDF"),
        ("02", "Paste the job description"),
        ("03", "Click Optimize Resume"),
        ("04", "Download your new PDF"),
    ]
    for num, title in steps:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-label">Step {num}</div>
            <div class="step-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown('<h1 class="main-header">📄 AI ATS Resume Optimizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Tailor your resume to any job description — naturally, honestly, and ATS-ready.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    ⚠️ <strong>Important:</strong> The AI is strictly instructed <em>not</em> to invent or hallucinate experience.
    It only reorganises and rewords what is already in your resume to better match the job's keywords.
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ─────────────────────────────────────────────
# Main Inputs
# ─────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📎 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Drop your PDF resume here",
        type=["pdf"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.markdown(f'<div class="success-box">✅ <strong>{uploaded_file.name}</strong> uploaded successfully.</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 💼 Paste the Job Description")
    job_description = st.text_area(
        "Job Description",
        height=260,
        placeholder="Paste the full job description here — including required skills, responsibilities, and qualifications...",
        label_visibility="collapsed"
    )

st.markdown("---")


# ─────────────────────────────────────────────
# Helper: Extract text from PDF
# ─────────────────────────────────────────────
def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts).strip()


# ─────────────────────────────────────────────
# Helper: Call OpenAI
# ─────────────────────────────────────────────
def optimize_resume_with_ai(resume_text: str, jd_text: str, api_key: str, model: str) -> str:
    client = openai.OpenAI(api_key=api_key)

    system_prompt = """You are an expert ATS (Applicant Tracking System) resume writer and career coach with 15+ years of experience.

Your task is to rewrite the candidate's resume to maximise its match against the provided Job Description (JD).

STRICT RULES — you MUST follow these without exception:
1. DO NOT invent, fabricate, or hallucinate ANY experience, skill, qualification, project, metric, or fact that is not explicitly present in the original resume. This is a hard requirement.
2. Only use real information from the candidate's resume. Rephrase, reorder, and highlight — but never add fictional content.
3. Naturally incorporate high-value keywords, hard skills, soft skills, and phrases extracted from the JD into the rewritten bullet points where they authentically apply.
4. Strengthen weak or vague bullet points using the STAR framework (Situation, Task, Action, Result) only when the original text provides enough information to do so.
5. Remove irrelevant experience that doesn't serve the target role.
6. Output the resume in clean plain text with clear section headings in UPPERCASE (e.g., SUMMARY, EXPERIENCE, SKILLS, EDUCATION, CERTIFICATIONS).
7. Use "•" for bullet points. Keep the layout simple, linear, and single-column for ATS compatibility.
8. Do not include any preamble, commentary, or explanation — output ONLY the optimised resume text.
9. Preserve the candidate's real name, contact information, and dates exactly as they appear in the original.
10. Write in a professional, confident, and concise tone.
"""

    user_prompt = f"""Here is the candidate's original resume:

--- RESUME START ---
{resume_text}
--- RESUME END ---

Here is the target Job Description:

--- JOB DESCRIPTION START ---
{jd_text}
--- JOB DESCRIPTION END ---

Please rewrite the resume following all the rules in your instructions. Output only the optimised resume text."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=3000,
    )

    return response.choices[0].message.content.strip()


# ─────────────────────────────────────────────
# Helper: Generate ATS-friendly PDF
# ─────────────────────────────────────────────
def generate_pdf(optimized_text: str) -> bytes:
    """
    Produces a clean, single-column, ATS-friendly PDF.
    Uses fpdf2 with Unicode support via the built-in Helvetica family.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(left=20, top=20, right=20)

    lines = optimized_text.split("\n")

    for line in lines:
        stripped = line.strip()

        if not stripped:
            pdf.ln(3)
            continue

        # Detect ALL-CAPS section heading
        if stripped.isupper() and len(stripped) < 60 and not stripped.startswith("•"):
            pdf.ln(2)
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.set_text_color(30, 30, 30)
            pdf.cell(0, 8, stripped, new_x="LMARGIN", new_y="NEXT")
            # Underline via a thin rule
            pdf.set_draw_color(99, 102, 241)
            pdf.set_line_width(0.5)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 170, pdf.get_y())
            pdf.ln(2)

        # Bullet point lines
        elif stripped.startswith("•") or stripped.startswith("-"):
            content = stripped.lstrip("•- ").strip()
            pdf.set_font("Helvetica", size=9.5)
            pdf.set_text_color(50, 50, 50)
            # Indent + bullet
            pdf.set_x(24)
            pdf.multi_cell(
                w=166,
                h=5.5,
                text=f"\u2022  {content}",
                new_x="LMARGIN",
                new_y="NEXT"
            )
            pdf.ln(0.5)

        else:
            # Regular text / sub-headings (e.g. "Company | Role | Date")
            # Heuristic: if it contains "|" or ends with digits (date), treat as sub-heading
            is_subheading = ("|" in stripped or re.search(r"\d{4}", stripped))
            if is_subheading:
                pdf.set_font("Helvetica", style="B", size=10)
                pdf.set_text_color(30, 30, 30)
            else:
                pdf.set_font("Helvetica", size=9.5)
                pdf.set_text_color(60, 60, 60)

            pdf.set_x(20)
            pdf.multi_cell(0, 5.8, stripped, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.5)

    return bytes(pdf.output())


# ─────────────────────────────────────────────
# Optimize Button + Output
# ─────────────────────────────────────────────
col_btn, _ = st.columns([1, 2])
with col_btn:
    optimize_clicked = st.button("🚀 Optimize Resume", use_container_width=True)

if optimize_clicked:
    # ── Validation ──────────────────────────────
    errors = []
    if not api_key:
        errors.append("🔑 Please enter your OpenAI API key in the sidebar.")
    if not uploaded_file:
        errors.append("📎 Please upload your PDF resume.")
    if not job_description.strip():
        errors.append("💼 Please paste the target Job Description.")

    if errors:
        for err in errors:
            st.error(err)
        st.stop()

    # ── Step 1: Extract PDF text ─────────────────
    with st.spinner("📖 Reading your resume PDF..."):
        try:
            pdf_bytes = uploaded_file.read()
            resume_text = extract_text_from_pdf(pdf_bytes)
        except Exception as e:
            st.error(f"❌ Failed to read PDF: {e}")
            st.stop()

    if not resume_text:
        st.error("❌ Could not extract any text from the PDF. Please ensure it is a text-based (not scanned/image) PDF.")
        st.stop()

    with st.expander("🔍 Extracted Resume Text (preview)", expanded=False):
        st.text_area("Raw extracted text", value=resume_text, height=200, disabled=True)

    # ── Step 2: AI Processing ────────────────────
    with st.spinner(f"🤖 Optimizing your resume with {model_choice}… this may take 20–40 seconds…"):
        try:
            optimized_text = optimize_resume_with_ai(
                resume_text=resume_text,
                jd_text=job_description,
                api_key=api_key,
                model=model_choice,
            )
        except openai.AuthenticationError:
            st.error("❌ Invalid OpenAI API key. Please check and try again.")
            st.stop()
        except openai.RateLimitError:
            st.error("❌ OpenAI rate limit reached. Please wait a moment and try again.")
            st.stop()
        except openai.OpenAIError as e:
            st.error(f"❌ OpenAI API error: {e}")
            st.stop()

    st.markdown("""
    <div class="success-box">
        ✅ <strong>AI optimization complete!</strong> Review your optimized resume below, then download the ATS-ready PDF.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📝 Optimized Resume Text (preview)", expanded=True):
        st.text_area("Optimized resume", value=optimized_text, height=400, disabled=True)

    # ── Step 3: Generate PDF ─────────────────────
    with st.spinner("📄 Generating your ATS-optimized PDF..."):
        try:
            pdf_output = generate_pdf(optimized_text)
        except Exception as e:
            st.error(f"❌ Failed to generate PDF: {e}")
            st.stop()

    # ── Step 4: Download Button ──────────────────
    st.markdown("---")
    st.markdown("### ⬇️ Download Your Optimized Resume")

    original_name = uploaded_file.name.replace(".pdf", "")
    download_filename = f"{original_name}_ATS_Optimized.pdf"

    st.download_button(
        label="⬇️ Download ATS-Optimized PDF",
        data=pdf_output,
        file_name=download_filename,
        mime="application/pdf",
        use_container_width=True,
    )

    st.markdown("""
    <div class="info-box">
        💡 <strong>Tip:</strong> Test your new resume at <a href="https://www.jobscan.co" target="_blank">Jobscan.co</a>
        or <a href="https://resume.io" target="_blank">Resume.io</a> to verify your ATS match score.
    </div>
    """, unsafe_allow_html=True)
