def get_attack_prompt(scenario_name):
    prompt = f"""
    You are an expert cybersecurity dataset generator. 
    Generate a realistic process-command dataset for the following scenario: {scenario_name}.
    
    Requirements:
    1. Total rows: Approximately 220 rows.
    2. Exactly 20 rows must be 'malicious' and logically simulate the attack scenario from start to finish.
    3. Approximately 200 rows must be 'benign' background noise (normal OS activity).
    4. Output MUST be in valid CSV format with exactly these three columns: process_name, command_line, label.
    5. Separate from the CSV, provide a brief 'attack_story' explaining the narrative.
    
    Return the response in a structured JSON format with two keys: 'csv_data' and 'attack_story'.
    """
    return prompt