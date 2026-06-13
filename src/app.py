import streamlit as st
import os
import json
import re
import pandas as pd
from datetime import datetime
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Red Team Generator",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] {
    background-color: #f5f5f7 !important;
    color: #1d1d1f !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif !important;
  }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 760px !important;
  }

  .hero {
    background: #1d1d1f;
    border-radius: 18px;
    padding: 2.6rem 2.5rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
  }
  .hero-eyebrow {
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #ff453a; margin-bottom: 0.6rem;
  }
  .hero h1 {
    font-size: 2.6rem; font-weight: 700;
    color: #f5f5f7; letter-spacing: -0.03em;
    line-height: 1.1; margin: 0 0 0.6rem 0;
  }
  .hero-sub { font-size: 0.9rem; color: #86868b; }
  .hero-badge {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(255,69,58,0.12);
    border: 1px solid rgba(255,69,58,0.25);
    color: #ff453a; font-size: 11px; font-weight: 600;
    padding: 5px 14px; border-radius: 6px;
    margin-top: 1.1rem; letter-spacing: 0.06em; text-transform: uppercase;
  }
  .dot-live {
    width: 6px; height: 6px; background: #ff453a;
    border-radius: 50%; display: inline-block;
    animation: blink 1.5s infinite;
  }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

  .section-label {
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.09em; text-transform: uppercase;
    color: #86868b; margin-bottom: 0.4rem; margin-top: 1.2rem;
    display: block;
  }

  /* inputs */
  .stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1.5px solid #e0e0e5 !important;
    border-radius: 10px !important;
    color: #1d1d1f !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #0071e3 !important;
    box-shadow: 0 0 0 3px rgba(0,113,227,0.1) !important;
  }
  .stTextInput > div > div > input::placeholder { color: #aeaeb2 !important; }

  /* all buttons red, same size */
  .stButton > button {
    background: #ff3b30 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 9px 10px !important;
    width: 100% !important;
    height: 40px !important;
    min-height: 40px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    transition: background 0.15s !important;
  }
  .stButton > button:hover { background: #e0332a !important; }
  .stButton > button:active { background: #cc2f26 !important; }

  /* stats */
  .stat-grid {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 10px; margin: 1.4rem 0;
  }
  .stat-item {
    background: #fff; border-radius: 12px;
    padding: 1rem; text-align: center;
    border: 1px solid rgba(0,0,0,0.06);
  }
  .stat-num { font-size: 1.9rem; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }
  .stat-lbl { font-size: 10px; font-weight: 500; color: #86868b; margin-top: 4px; text-transform: uppercase; }
  .c-blue{color:#0071e3} .c-red{color:#ff3b30} .c-green{color:#34c759} .c-orange{color:#ff9500}

  .story-box {
    background: #fff;
    border-left: 3px solid #ff3b30;
    border-radius: 0 10px 10px 0;
    padding: 1.1rem 1.3rem;
    font-size: 13.5px; line-height: 1.75;
    color: #3a3a3c; margin-bottom: 1.2rem;
    border-top: 1px solid rgba(0,0,0,0.06);
    border-right: 1px solid rgba(0,0,0,0.06);
    border-bottom: 1px solid rgba(0,0,0,0.06);
  }

  .terminal {
    background: #1c1c1e; border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'SF Mono','Menlo',monospace;
    font-size: 12px; color: #34c759;
    min-height: 52px; line-height: 1.9;
    margin-top: 0.4rem;
  }

  .stTabs [data-baseweb="tab-list"] {
    background: #ebebed !important; border-radius: 10px !important;
    padding: 3px !important; gap: 2px !important; border: none !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 8px !important;
    color: #86868b !important; font-weight: 500 !important;
    font-size: 13px !important; border: none !important;
  }
  .stTabs [aria-selected="true"] {
    background: #fff !important; color: #1d1d1f !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
  }

  .err {
    background: #fff2f2; border: 1px solid #ffd0cc;
    border-radius: 10px; padding: 10px 14px;
    color: #c0392b; font-size: 13px; margin-top: 0.5rem;
  }
  hr { border-color: rgba(0,0,0,0.07) !important; }

  /* hide the label above text inputs completely */
  .stTextInput label { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ── helpers ───────────────────────────────────────────────────────────────────
def call_gemini(prompt, api_key):
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    r = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.9, max_output_tokens=8192))
    return r.text

def parse_response(raw):
    text = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    text = re.sub(r"\s*```$", "", text).strip()
    s, e = text.find("{"), text.rfind("}") + 1
    if s == -1 or e == 0: raise ValueError("No JSON in response.")
    return json.loads(text[s:e])

def validate_csv(csv_str):
    df = pd.read_csv(StringIO(csv_str))
    missing = {"process_name", "command_line", "label"} - set(df.columns)
    if missing: raise ValueError(f"Missing columns: {missing}")
    df["label"] = df["label"].str.strip().str.lower()
    return df

def build_prompt(scenario):
    return f"""You are an expert cybersecurity red team dataset generator. Generate a REALISTIC and EVASIVE process-command dataset for: "{scenario}".

RULES:
1. EXACTLY 220 data rows + 1 header = 221 lines total.
2. EXACTLY 20 rows labeled 'malicious' — coherent attack story (initial access → execution → escalation → objective).
3. EXACTLY 200 rows labeled 'benign' — realistic OS background noise.
4. Malicious commands must be EVASIVE: use LOLBins (certutil, wmic, mshta, regsvr32, rundll32, schtasks, net, sc, powershell) with realistic args that blend in.
5. Spread malicious rows throughout — NOT clustered.
6. Benign rows: diverse, mix Windows and Linux processes.

Return ONLY valid JSON with keys "csv_data" and "attack_story". No markdown, no extra text."""


# ── page ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Bootcamp · Jun 2026</div>
  <h1>Red Team Attack Generator</h1>
  <div class="hero-sub">Generate realistic, evasive process-command attack datasets on demand.</div>
  <div class="hero-badge"><span class="dot-live"></span>Attacker Mode Active</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<span class="section-label">API Key</span>', unsafe_allow_html=True)
api_key_input = st.text_input("API Key", type="password", placeholder="Paste your Gemini API key...", label_visibility="collapsed")

st.markdown('<span class="section-label">Attack Scenario</span>', unsafe_allow_html=True)
scenario_input = st.text_input("Scenario", placeholder="e.g. ransomware, lateral_movement, crypto_miner...",
    label_visibility="collapsed", value=st.session_state.get("scenario_preset", ""))

st.markdown('<span class="section-label">Quick Pick</span>', unsafe_allow_html=True)
presets = ["ransomware", "lateral_movement", "credential_dumping", "crypto_miner",
           "data_exfiltration", "persistence", "privilege_escalation"]
cols = st.columns(4)
for i, p in enumerate(presets):
    if cols[i % 4].button(p, key=f"p_{p}"):
        st.session_state["scenario_preset"] = p
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
generate_btn = st.button("Generate Attack Dataset", use_container_width=True)

st.markdown('<span class="section-label">Live Log</span>', unsafe_allow_html=True)
log_box = st.empty()
log_box.markdown('<div class="terminal">Waiting for input...</div>', unsafe_allow_html=True)


# ── generation ────────────────────────────────────────────────────────────────
if generate_btn:
    api_key = api_key_input.strip() or os.getenv("GEMINI_API_KEY", "")
    scenario = scenario_input.strip()

    if not api_key:
        log_box.markdown('<div class="err">No API key. Paste your Gemini key above or add it to .env</div>', unsafe_allow_html=True)
    elif not scenario:
        log_box.markdown('<div class="err">Enter a scenario name or click a Quick Pick button.</div>', unsafe_allow_html=True)
    else:
        logs = []
        def log(m):
            logs.append(m)
            log_box.markdown('<div class="terminal">' + "<br>".join(logs) + "</div>", unsafe_allow_html=True)

        try:
            log(f"→ Scenario: {scenario}")
            log("→ Calling Gemini API...")
            raw = call_gemini(build_prompt(scenario), api_key)
            log("→ Parsing response...")
            data = parse_response(raw)
            csv_data = data.get("csv_data", "")
            story = data.get("attack_story", "")
            if not csv_data: raise ValueError("Empty csv_data.")
            log("→ Validating CSV...")
            df = validate_csv(csv_data)
            mal = int((df["label"] == "malicious").sum())
            ben = int((df["label"] == "benign").sum())
            total = len(df)
            log(f"→ {total} rows | {mal} malicious | {ben} benign")

            os.makedirs("output", exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe = scenario.replace(" ", "_")
            df.to_csv(f"output/{safe}_{ts}.csv", index=False)
            with open(f"output/{safe}_{ts}_story.txt", "w") as f:
                f.write(f"ATTACK SCENARIO: {scenario}\n{'='*60}\n\n{story}")
            mal_df = df[df["label"] == "malicious"][["process_name", "command_line"]]
            mal_df.to_csv(f"output/{safe}_{ts}_groundtruth.csv", index=False)
            log("✓ Done — attack generated successfully")

            st.session_state["result"] = {
                "scenario": scenario, "df": df, "mal_df": mal_df, "story": story,
                "csv_data": csv_data, "gt_csv": mal_df.to_csv(index=False),
                "scored_csv": df[["process_name", "command_line"]].to_csv(index=False),
                "mal": mal, "ben": ben, "total": total,
            }
        except Exception as e:
            log(f"✗ Error: {str(e)}")


# ── results ───────────────────────────────────────────────────────────────────
if "result" in st.session_state:
    r = st.session_state["result"]

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-item"><div class="stat-num c-blue">{r['total']}</div><div class="stat-lbl">Total rows</div></div>
      <div class="stat-item"><div class="stat-num c-red">{r['mal']}</div><div class="stat-lbl">Malicious</div></div>
      <div class="stat-item"><div class="stat-num c-green">{r['ben']}</div><div class="stat-lbl">Benign</div></div>
      <div class="stat-item"><div class="stat-num c-orange">{round(r['mal']/r['total']*100,1)}%</div><div class="stat-lbl">Attack ratio</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="section-label">Attack Story</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="story-box">{r["story"]}</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Full Dataset", "Malicious Commands", "Ground Truth (Judges)"])
    with tab1:
        st.dataframe(r["df"], use_container_width=True, height=340)
        st.download_button("Download full CSV", data=r["csv_data"], file_name=f"{r['scenario']}_dataset.csv", mime="text/csv")
    with tab2:
        st.dataframe(r["mal_df"], use_container_width=True, height=340)
        st.caption(f"{r['mal']} malicious commands — the full attack chain")
    with tab3:
        st.markdown("Submit this file to the judges — your 20 malicious commands, no labels.")
        st.dataframe(r["mal_df"], use_container_width=True, height=280)
        st.download_button("Download ground truth CSV", data=r["gt_csv"], file_name=f"{r['scenario']}_groundtruth.csv", mime="text/csv")

    st.markdown("---")
    st.markdown('<span class="section-label">Scored CSV for Blue Team (labels stripped)</span>', unsafe_allow_html=True)
    st.download_button("Download scored CSV", data=r["scored_csv"], file_name=f"{r['scenario']}_scored.csv", mime="text/csv")
