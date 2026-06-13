# ⚔️ Red Team Attack Generator
> AI Red Team vs Blue Team Bootcamp · Jun 2026

Generates realistic, evasive process-command attack datasets on demand using Gemini AI. Built for the Red Team challenge — given any attack scenario, produces a 220-row CSV with 20 hidden malicious commands and a written attack story.

---

## Quick Start

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Add your Gemini API key
Open `.env` and replace the placeholder:
```
GEMINI_API_KEY=your_actual_key_here
```
> You can also skip this and paste the key directly in the UI each time.

### 3. Run
```bash
streamlit run src/app.py
```
Opens automatically at **http://localhost:8501**

---

## How to use the UI

1. Paste your Gemini API key (or leave empty if set in `.env`)
2. Type a scenario name — or click one of the **Quick Pick** buttons
3. Hit **Generate Attack Dataset**
4. Watch the live log as Gemini generates the attack
5. Review the results — stats, attack story, and data tables
6. Download the files you need (see below)

---

## Output files

All files are saved to `output/` automatically, and available as downloads in the UI.

| File | Who gets it |
|------|-------------|
| `{scenario}_dataset.csv` | You keep this (full data with labels) |
| `{scenario}_story.txt` | Use for your demo pitch |
| `{scenario}_groundtruth.csv` | Give to the **judges** (20 malicious commands) |
| `{scenario}_scored.csv` | Give to the **Blue Team** (labels stripped) |

---

## Project structure

```
ai-redteam-generator/
├── src/
│   ├── app.py          ← Streamlit UI (run this)
│   ├── generator.py    ← Core logic — calls Gemini, validates CSV, saves files
│   ├── prompts.py      ← LLM prompt templates
│   └── __init__.py
├── main.py             ← CLI alternative (no UI)
├── .env                ← Your API key goes here
├── requirements.txt
└── output/             ← Generated files appear here
```

---

## What the tool generates

Each run produces:
- **220 rows** — 20 malicious + 200 benign background noise
- **Evasive commands** — malicious rows use real LOLBins (certutil, schtasks, wmic, rundll32) that blend in with normal activity
- **Coherent attack story** — initial access → execution → escalation → objective
- **Random distribution** — malicious rows are spread across the dataset, not clustered

---

## Requirements

- Python 3.9+
- Gemini API key — get one free at [aistudio.google.com](https://aistudio.google.com)
