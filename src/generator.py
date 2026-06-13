import os
import json
import re
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

from src.prompts import get_attack_prompt

load_dotenv()


class AttackGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment. Add it to your .env file.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def _call_llm(self, prompt: str) -> str:
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=8192,
            ),
        )
        return response.text

    def _parse_response(self, raw: str) -> dict:
        text = raw.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in LLM response.")
        return json.loads(text[start:end])

    def _validate_csv(self, csv_data: str) -> pd.DataFrame:
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        required_cols = {"process_name", "command_line", "label"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"CSV missing columns. Got: {list(df.columns)}")
        malicious_count = (df["label"] == "malicious").sum()
        benign_count = (df["label"] == "benign").sum()
        if malicious_count != 20:
            raise ValueError(f"Expected exactly 20 malicious rows, got {malicious_count}")
        if benign_count < 190:
            raise ValueError(f"Expected ~200 benign rows, got {benign_count}")
        return df

    def generate_scenario(self, scenario: str, output_dir: str = "output") -> tuple:
        print(f"\n⚔️  Generating attack for scenario: '{scenario}'...")
        print("📡 Calling Gemini API (this may take 15-30 seconds)...")
        prompt = get_attack_prompt(scenario)
        raw = self._call_llm(prompt)
        print("🔍 Parsing response...")
        data = self._parse_response(raw)
        csv_data = data.get("csv_data", "")
        attack_story = data.get("attack_story", "")
        if not csv_data:
            raise ValueError("LLM returned empty csv_data.")
        print("✅ Validating CSV structure...")
        df = self._validate_csv(csv_data)
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_scenario = scenario.replace(" ", "_").replace("/", "-")
        csv_path = os.path.join(output_dir, f"{safe_scenario}_{timestamp}.csv")
        story_path = os.path.join(output_dir, f"{safe_scenario}_{timestamp}_story.txt")
        malicious_path = os.path.join(output_dir, f"{safe_scenario}_{timestamp}_groundtruth.csv")
        df.to_csv(csv_path, index=False)
        with open(story_path, "w") as f:
            f.write(f"ATTACK SCENARIO: {scenario}\n{'='*60}\n\n{attack_story}")
        malicious_df = df[df["label"] == "malicious"][["process_name", "command_line"]]
        malicious_df.to_csv(malicious_path, index=False)
        print(f"\n📁 Outputs saved to {output_dir}/")
        print(f"📊 {len(df)} rows | {(df['label']=='malicious').sum()} malicious | {(df['label']=='benign').sum()} benign")
        return csv_path, story_path