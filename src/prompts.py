def get_attack_prompt(scenario_name: str) -> str:
    prompt = f"""
You are an expert cybersecurity red team dataset generator. Your job is to create a REALISTIC and EVASIVE process-command dataset for the following attack scenario: "{scenario_name}".

CRITICAL RULES:
1. Generate EXACTLY 220 rows total.
2. EXACTLY 20 rows must be labeled 'malicious'. These must tell a coherent attack story with a clear beginning, middle, and end.
3. EXACTLY 200 rows must be labeled 'benign'. These are normal background OS noise (antivirus scans, system updates, browser activity, office apps, etc).
4. The 20 malicious commands must be EVASIVE — they should blend in with normal activity. Use:
   - Living-off-the-land binaries (LOLBins) like certutil, wmic, mshta, regsvr32, rundll32, schtasks, net, sc
   - Realistic-looking process names (never invent fake ones)
   - Commands that look like admin tasks but do something malicious
   - Vary the command lengths and argument styles so they don't stand out
5. The benign commands must be realistic and varied — mix Windows AND Linux processes, everyday apps, system services.
6. The malicious commands must be spread across the dataset (not all at the top or bottom), interspersed with benign ones.

OUTPUT FORMAT: Return ONLY a valid JSON object with exactly two keys:
- "csv_data": a string containing valid CSV with exactly these columns: process_name,command_line,label
- "attack_story": a string (2-4 paragraphs) narrating the attack from initial access to final objective

The CSV must:
- Have a header row: process_name,command_line,label
- Use double quotes around any field that contains a comma
- Have no extra whitespace or markdown
- Have EXACTLY 221 lines (1 header + 220 data rows)

Do NOT include any text outside the JSON object. No markdown, no backticks, no explanation.
"""
    return prompt