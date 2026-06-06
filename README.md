# 📄 AI ATS Resume Optimizer

> Tailor your resume to any job description — naturally, honestly, and ATS-ready — powered by OpenAI GPT.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [The Problem](#-the-problem)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the App](#-running-the-app)
- [How to Use](#-how-to-use)
- [How It Works](#-how-it-works)
- [AI Prompt Design](#-ai-prompt-design)
- [PDF Generation](#-pdf-generation)
- [Configuration](#-configuration)
- [Important Notes](#-important-notes)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧭 Overview

**AI ATS Resume Optimizer** is a Streamlit web application that uses OpenAI's GPT models to automatically rewrite your resume to match any job description. It extracts keywords, skills, and phrases from the job posting and naturally weaves them into your existing resume content — without fabricating any experience. The final result is exported as a clean, single-column, ATS-parseable PDF ready for submission.

---

## 🎯 The Problem

Most resumes are rejected before a human ever reads them.

Companies use **Applicant Tracking Systems (ATS)** — software that scans resumes for keywords matching the job posting. If your resume doesn't contain the right terms (even if you have the right experience), it gets filtered out automatically.

Manually rewriting your resume for every job is tedious and time-consuming. This app automates the entire process in under a minute.

---

## ✨ Features

- 🔑 **Secure API key input** — entered per-session in the sidebar, never stored or logged
- 📎 **PDF resume upload** — robust text extraction via `pdfplumber`
- 💼 **Job description analysis** — GPT extracts hard skills, soft skills, tools, and role-specific phrases
- ✍️ **Intelligent rewriting** — bullet points are rephrased to naturally incorporate JD keywords
- 🚫 **No hallucination** — AI is strictly instructed never to invent experience or qualifications
- 📄 **ATS-safe PDF output** — single-column, standard font, no tables or graphics that confuse parsers
- 👁️ **Live text preview** — see both the extracted and optimized resume text before downloading
- ⚙️ **Model selector** — choose `gpt-4o-mini`, `gpt-3.5-turbo`, or `gpt-4o`
- 🔄 **Status feedback** — spinners and messages keep you informed at every step
- ⬇️ **One-click download** — get your optimized PDF instantly

---

## 🛠 Tech Stack

| Layer            | Library / Tool         | Purpose                                      |
|------------------|------------------------|----------------------------------------------|
| UI Framework     | `streamlit`            | Web interface, file upload, download button  |
| PDF Parsing      | `pdfplumber`           | Robust text extraction from uploaded PDFs    |
| AI Engine        | `openai`               | GPT-powered resume rewriting                 |
| PDF Generation   | `fpdf2`                | Generating clean, ATS-friendly output PDFs   |
| Image Support    | `Pillow`               | Required by fpdf2 for image handling         |

---

## 📁 Project Structure

```
ai-ats-resume-optimizer/
│
├── app.py              # Main Streamlit application (single file)
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

---

## ✅ Prerequisites

- Python **3.8 or higher**
- An **OpenAI API key** — get one at [platform.openai.com](https://platform.openai.com/api-keys)
- A **text-based PDF resume** (not a scanned image — those require OCR)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-ats-resume-optimizer.git
cd ai-ats-resume-optimizer
```

### 2. Create a virtual environment (recommended)

```bash
# Create
python -m venv venv

# Activate — macOS/Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit openai pdfplumber fpdf2 Pillow
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

**`requirements.txt` contents:**
```
streamlit>=1.32.0
openai>=1.0.0
pdfplumber>=0.10.0
fpdf2>=2.7.0
Pillow>=10.0.0
```

---

## 🚀 Running the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at:
```
http://localhost:8501
```

---

## 📖 How to Use

### Step 1 — Enter Your API Key
In the **left sidebar**, paste your OpenAI API key into the secure input field. It is used only for this session and is never stored.

### Step 2 — Choose a Model
Select your preferred GPT model from the dropdown:

| Model | Speed | Cost | Quality |
|-------|-------|------|---------|
| `gpt-4o-mini` ⭐ | Fast | Lowest | Great |
| `gpt-3.5-turbo` | Fast | Low | Good |
| `gpt-4o` | Slower | Higher | Best |

> **Recommended:** `gpt-4o-mini` offers the best balance of speed, cost, and quality for resume-length content.

### Step 3 — Upload Your Resume
Click the file uploader and select your current resume in **PDF format**.

### Step 4 — Paste the Job Description
Copy the full job description from the job posting (including skills, responsibilities, and qualifications) and paste it into the text area.

### Step 5 — Optimize
Click **🚀 Optimize Resume**. The app will:
1. Extract text from your PDF
2. Send it to GPT along with the JD
3. Display the optimized resume text as a preview
4. Generate an ATS-friendly PDF

### Step 6 — Download
Click **⬇️ Download ATS-Optimized PDF** to save your new resume. The file is automatically named `[your-original-filename]_ATS_Optimized.pdf`.

---

## ⚙️ How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  Upload PDF     │────▶│  pdfplumber      │────▶│  Extracted Text   │
│  Resume         │     │  Text Extraction │     │  (raw string)     │
└─────────────────┘     └──────────────────┘     └────────┬──────────┘
                                                           │
┌─────────────────┐                                        │
│  Paste Job      │────────────────────────────────────────▼
│  Description    │                              ┌───────────────────┐
└─────────────────┘                              │  OpenAI GPT API   │
                                                 │  (gpt-4o-mini)    │
                                                 └────────┬──────────┘
                                                          │
                                                          ▼
                                                 ┌───────────────────┐
                                                 │  Optimized Resume │
                                                 │  (plain text)     │
                                                 └────────┬──────────┘
                                                          │
                                                          ▼
                                                 ┌───────────────────┐
                                                 │  fpdf2            │
                                                 │  PDF Generation   │
                                                 └────────┬──────────┘
                                                          │
                                                          ▼
                                                 ┌───────────────────┐
                                                 │  ⬇️ Download PDF  │
                                                 └───────────────────┘
```

---

## 🧠 AI Prompt Design

The GPT system prompt enforces **10 strict rules**, the most important being:

| Rule | Description |
|------|-------------|
| 🚫 No hallucination | Absolutely forbidden from inventing experience, skills, or metrics |
| 🔑 Keyword integration | Naturally incorporates JD keywords where they genuinely apply |
| ⭐ STAR framework | Strengthens vague bullets using Situation-Task-Action-Result only when source material supports it |
| 🗂️ Structured output | Outputs UPPERCASE section headings, bullet points with `•`, clean plain text |
| 🧾 Preserve facts | Name, contact info, and dates are preserved verbatim |

**Temperature is set to `0.4`** — disciplined enough to avoid fabrication, flexible enough for natural rephrasing.

---

## 📄 PDF Generation

The `generate_pdf()` function applies three rendering rules per line:

| Line Type | Detection | Rendering |
|-----------|-----------|-----------|
| **Section heading** | All uppercase, < 60 chars | Bold, 11pt, with indigo underrule |
| **Bullet point** | Starts with `•` or `-` | Indented, Unicode bullet, 9.5pt |
| **Sub-heading** | Contains `\|` or a 4-digit year | Bold, 10pt |
| **Body text** | Everything else | Regular, 9.5pt |

Font: **Helvetica** (universally ATS-safe, no embedding issues)
Layout: **Single column**, 20mm margins, auto page break at 18mm from bottom

---

## 🔧 Configuration

You can adjust these values directly in `app.py`:

| Setting | Location | Default | Description |
|---------|----------|---------|-------------|
| Default model | `model_choice` selectbox | `gpt-4o-mini` | GPT model used |
| Temperature | `optimize_resume_with_ai()` | `0.4` | AI creativity level (0 = deterministic) |
| Max tokens | `optimize_resume_with_ai()` | `3000` | Max length of AI response |
| Page margins | `generate_pdf()` | `20mm` | PDF page margins |
| Font size | `generate_pdf()` | `9.5pt` body | PDF body font size |

---

## ⚠️ Important Notes

1. **Text-based PDFs only** — scanned or image-based PDFs will return no text. Use a PDF created from a Word doc, Google Doc, or similar.
2. **Your API key is not stored** — it exists only in the current browser session's memory.
3. **OpenAI costs** — a single resume optimization with `gpt-4o-mini` typically costs **$0.001–$0.005** (a fraction of a cent).
4. **Review before sending** — always read the optimized resume before submitting. AI rephrasing should be verified for accuracy.
5. **ATS tip** — test your final resume at [Jobscan.co](https://www.jobscan.co) or [Resume.io](https://resume.io) to verify your match score.

---

## 🐛 Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "Could not extract any text" | Scanned/image PDF | Use a text-based PDF (convert from Word/Google Docs) |
| "Invalid API key" | Wrong or expired key | Re-check your key at platform.openai.com |
| "Rate limit reached" | Too many API calls | Wait 30–60 seconds and retry |
| Garbled PDF text | Special characters | Ensure your resume uses standard Unicode characters |
| App won't start | Missing dependency | Run `pip install streamlit openai pdfplumber fpdf2 Pillow` |
| Blank output PDF | Empty AI response | Try a different model or shorten the job description |

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas for improvements:

- [ ] Add support for `.docx` resume uploads
- [ ] Add a match score display (% keyword overlap before/after)
- [ ] Support multiple output formats (Word, plain text)
- [ ] Add a cover letter generator using the same JD
- [ ] Implement session history to compare versions
- [ ] Add OCR support for scanned PDFs via `pytesseract`

To contribute:
```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request
```

---

## 📜 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it with attribution.

```
MIT License — Copyright (c) 2024
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software.
```

---

## 🙏 Acknowledgements

- [OpenAI](https://openai.com) — for the GPT API
- [Streamlit](https://streamlit.io) — for the rapid UI framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) — for reliable PDF text extraction
- [fpdf2](https://py-fpdf2.readthedocs.io) — for clean PDF generation

---

<div align="center">
  <p>Built with ❤️ using Python, Streamlit, and OpenAI</p>
  <p>
    <a href="https://platform.openai.com/api-keys">Get OpenAI API Key</a> •
    <a href="https://www.jobscan.co">Test ATS Score</a> •
    <a href="https://streamlit.io">Learn Streamlit</a>
  </p>
</div>
