#!/usr/bin/env python3
"""
Self-Healing Endpoint Remediation Agent (HITL Engine)
Document ID: AGENT-REMED-003
Owner: IT Operations & Information Security

Description:
    Ingests endpoint security compliance audit JSON logs, uses Gemini to analyze 
    policy failures, determines required remediation steps (e.g., BitLocker enablement,
    MFA enforcement, session revocation), and generates a structured execution plan.
    Enforces Human-in-the-Loop (HITL) authorization prior to applying changes.

Usage:
    python ai-governance/workflows/remediation_agent.py --input audit_failure.json
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# 1. LLM REMEDIATION DIAGNOSTIC ENGINE (GOOGLE GEMINI API)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an Autonomous IT Remediation & Endpoint Security Agent.
You ingest endpoint compliance audit failures (JSON) and output a structured remediation plan.

Compliance Baselines: SOC 2 (CC6.8 - Flaw Remediation), NIST RMF (SI-2, AC-2), HIPAA ( 164.312).

Rules:
1. Determine if the failure severity requires Human-in-the-Loop (HITL) authorization. Any action affecting user sessions, disk encryption, or account status MUST require HITL approval.
2. Formulate a specific PowerShell execution command to remediate the failure.

Return ONLY a valid JSON object matching this exact schema:
{
  "target_device_or_user": "string",
  "compliance_gap": "string",
  "severity": "Low | Medium | High | Critical",
  "requires_hitl_approval": true,
  "recommended_powershell_payload": "string",
  "remediation_rationale": "string",
  "audit_framework_mapping": ["string", "string"]
}
"""

def generate_remediation_plan(audit_data: str, api_key: str) -> dict:
    """Queries Gemini 3.8 Flash to synthesize remediation plan from audit telemetry."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"{SYSTEM_PROMPT}\n\nAnalyze this compliance audit failure telemetry:\n{audit_data}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_text)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        sys.exit(f"[ERROR] Gemini API Request Failed: HTTP {e.code} - {error_body}")
    except Exception as e:
        sys.exit(f"[ERROR] Unexpected Error: {str(e)}")

# ---------------------------------------------------------------------------
# 2. AUDIT LOGGING & HITL EXECUTION GATE
# ---------------------------------------------------------------------------

def write_audit_trail(plan: dict, log_path: str = "ai-governance/remediation_audit.log"):
    """Appends an immutable JSON log of the remediation evaluation for SOC 2 audits."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": "AGENT-REMED-003",
        "evaluation": plan
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

# ---------------------------------------------------------------------------
# 3. MAIN EXECUTION PIPELINE
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Self-Healing Endpoint Remediation Agent")
    parser.add_argument("--input", required=True, help="Path to compliance audit failure JSON file")
    parser.add_argument("--auto-execute", action="store_true", help="Attempt execution if HITL is not required")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit("[ERROR] Environment variable GEMINI_API_KEY is not set.")

    if not os.path.exists(args.input):
        sys.exit(f"[ERROR] Input telemetry file not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        audit_content = f.read()

    print(f"[*] Ingesting audit failure telemetry from: {args.input}")
    print("[*] Generating AI remediation diagnostic payload...")
    
    plan = generate_remediation_plan(audit_content, api_key)
    write_audit_trail(plan)

    print("\n" + "="*60)
    print("===SELF-HEAVY ENDPOINT REMEDIATION PLAN===")
    print("="*60)
    print(f"Target Asset:          {plan.get('target_device_or_user')}")
    print(f"Compliance Gap:        {plan.get('compliance_gap')}")
    print(f"Severity Level:        {plan.get('severity')}")
    print(f"HITL Gate Required:    {plan.get('requires_hitl_approval')}")
    print(f"PowerShell Payload:    {plan.get('recommended_powershell_payload')}")
    print(f"Rationale:             {plan.get('remediation_rationale')}")
    print("Framework Mapping:")
    for fw in plan.get("audit_framework_mapping", []):
        print(f"  - {fw}")
    print("="*60)

    if plan.get("requires_hitl_approval"):
        print("\n[?? HITL GATE TRIGGERED] Remediation requires manual administrator approval.")
        print(f"Payload staged for execution approval: {plan.get('recommended_powershell_payload')}")
    else:
        print("\n[+] Low-risk policy failure. Payload cleared for automated orchestration.")

if __name__ == "__main__":
    main()
