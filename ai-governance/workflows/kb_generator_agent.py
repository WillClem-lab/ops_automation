#!/usr/bin/env python3
"""
Automated Knowledge Base & Runbook Generator Agent
Document ID: AGENT-KB-001
Owner: IT Operations & AI Governance

Description:
    Ingests raw incident notes, ticket logs, or unformatted post-mortem text,
    runs a pre-flight guardrail check to redact sensitive inputs (credentials, 
    IPs, PII/PHI), and invokes an LLM API to output a standardized, production-ready 
    Markdown Standard Operating Procedure (SOP) / Runbook.

Usage:
    python kb_generator_agent.py --input raw_ticket.txt --output docs/SOP_Remediation_Generated.md
"""

import os
import re
import sys
import json
import argparse
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# 1. PRE-FLIGHT GUARDRAILS & SANITIZATION ENGINE
# ---------------------------------------------------------------------------

PATTERNS = {
    "api_key": re.compile(r'(?i)(api[_-]?key|secret|bearer|password|passwd)\s*[:=]\s*["\']?([a-zA-Z0-9_\-\.]{8,})["\']?'),
    "ipv4": re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'),
    "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
}

def sanitize_input(text: str) -> tuple[str, int]:
    """
    Scans and redacts sensitive data categories prior to LLM processing.
    Returns sanitized text and total count of redacted items.
    """
    redaction_count = 0
    sanitized = text

    # Redact credentials/keys
    for match in PATTERNS["api_key"].finditer(sanitized):
        sanitized = sanitized.replace(match.group(2), "[REDACTED_CREDENTIAL]")
        redaction_count += 1

    # Redact IPv4 addresses
    ipv4_matches = PATTERNS["ipv4"].findall(sanitized)
    for ip in set(ipv4_matches):
        if not ip.startswith("127.0."):  # Keep loopback intact if needed
            sanitized = sanitized.replace(ip, "[REDACTED_IP_ADDRESS]")
            redaction_count += 1

    # Redact SSNs
    for ssn in set(PATTERNS["ssn"].findall(sanitized)):
        sanitized = sanitized.replace(ssn, "[REDACTED_SSN]")
        redaction_count += 1

    return sanitized, redaction_count

# ---------------------------------------------------------------------------
# 2. LLM EXECUTION ENGINE (ANTHROPIC CLAUDE API)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert IT Operations & Compliance Documentation Agent.
Your task is to take raw, sanitized incident triage notes and transform them into a clean, standard-compliant Markdown SOP / Runbook.

Mandatory Schema Requirements:
# Standard Operating Procedure: [Descriptive Title]
**Document ID:** SOP-AUTO-[Generated ID]
**Version:** 1.0
**Compliance Mapping:** SOC 2 (CC6.1, CC6.8), NIST RMF (AC-2, SI-2)

---

## 1. Executive Summary & Trigger Condition
[Summarize what happened and what triggers this procedure]

## 2. Environment & Affected Systems
[List affected operating systems, cloud providers, identity providers, or network assets]

## 3. Root Cause Analysis (RCA)
[Detailed explanation of why the failure occurred]

## 4. Step-by-Step Remediation Workflow
[Numbered, sequential steps with code blocks where applicable]

## 5. Prevention & Hardening Measures
[Proactive measures to ensure this issue does not recur]

Rules:
- Never invent missing server names or fake IPs; use placeholder variables like `<SERVER_NAME>` or `<TARGET_USER>` if details are vague.
- Enforce strict, clean Markdown formatting.
- Do not output introductory conversational text. Return ONLY the Markdown document.
"""

def query_claude_api(prompt_text: str, api_key: str) -> str:
    """
    Invokes Anthropic Claude API using standard Python library to avoid external dependency issues.
    """
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 2500,
        "system": SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"Transform these incident notes into an SOP:\n\n{prompt_text}"}
        ]
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        sys.exit(f"[ERROR] API Request Failed: HTTP {e.code} - {error_body}")
    except Exception as e:
        sys.exit(f"[ERROR] Unexpected Connection Error: {str(e)}")

# ---------------------------------------------------------------------------
# 3. MAIN EXECUTION PIPELINE
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Governed AI KB Runbook Generator Agent")
    parser.add_argument("--input", required=True, help="Path to raw incident log text file")
    parser.add_argument("--output", required=True, help="Path to save generated Markdown SOP")
    args = parser.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("[ERROR] Environment variable ANTHROPIC_API_KEY is not set.")

    if not os.path.exists(args.input):
        sys.exit(f"[ERROR] Input file not found: {args.input}")

    print(f"[*] Ingesting raw incident notes from: {args.input}")
    with open(args.input, "r", encoding="utf-8") as f:
        raw_content = f.read()

    print("[*] Running pre-flight privacy and credential redaction guardrails...")
    sanitized_content, redactions = sanitize_input(raw_content)
    print(f"[+] Guardrail Complete: Redacted {redactions} sensitive data instances.")

    print("[*] Querying Governed LLM Agent to synthesize SOP document...")
    markdown_output = query_claude_api(sanitized_content, api_key)

    # Ensure target output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(markdown_output)

    print(f"[SUCCESS] SOP successfully generated and written to: {args.output}")

if __name__ == "__main__":
    main()
