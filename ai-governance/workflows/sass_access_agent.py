#!/usr/bin/env python3
"""
Governed Access Request & Risk Evaluation Agent
Document ID: AGENT-RISK-002
Owner: IT Operations & Information Security

Description:
    Ingests end-user SaaS access requests, evaluates them against enterprise 
    governance rules (SSO/SCIM mandates, BAA requirements, PHI/PII exposure),
    scores security risk, and determines whether auto-approval or Human-in-the-Loop
    (HITL) IT/Security approval is required.

Usage:
    python ai-governance/workflows/saas_access_agent.py --request "I need an account for Notion AI to summarize patient notes"
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# 1. LLM RISK EVALUATION ENGINE (GOOGLE GEMINI API)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an Enterprise SaaS Governance & Identity Risk Evaluation Agent.
Your job is to analyze end-user requests for software access and return a structured JSON risk evaluation.

Compliance Context: SOC 2 (CC6.1, CC6.2, CC6.3), HIPAA Security Rule ( 164.312), NIST RMF (AC-2).

Governance Rules to Enforce:
1. Protected Health Information (PHI) / PII: If the user mentions patient data, PHI, or clinical notes, BAA (Business Associate Agreement) is MANDATORY. High Risk.
2. SSO/SCIM Mandate: Enterprise applications must support Entra ID / Okta Single Sign-On.
3. HITL Trigger: Any request with High or Medium risk, or involving unapproved AI tools, REQUIRES explicit Human-in-the-Loop (HITL) administrator approval.

Return ONLY a valid JSON object matching this exact schema:
{
  "app_name": "string",
  "intended_use_case": "string",
  "risk_score": "Low | Medium | High | Critical",
  "phi_pii_risk": true | false,
  "baa_required": true | false,
  "sso_enforcement_required": true | false,
  "approval_status": "AUTO_APPROVED | REQUIRES_HITL_APPROVAL | DENIED",
  "justification": "string",
  "recommended_security_controls": ["string", "string"]
}
"""

def evaluate_access_request(request_text: str, api_key: str) -> dict:
    """Queries Gemini 3.8 Flash to evaluate SaaS access request risk."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"{SYSTEM_PROMPT}\n\nEvaluate this access request:\n\"{request_text}\""
    
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
# 2. MAIN EXECUTION PIPELINE
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Governed Access Request & Risk Evaluation Agent")
    parser.add_argument("--request", required=True, help="User access request string")
    parser.add_argument("--output", help="Optional path to output JSON report")
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit("[ERROR] Environment variable GEMINI_API_KEY is not set.")

    print(f"[*] Ingesting access request: \"{args.request}\"")
    print("[*] Evaluating request against SOC 2 / HIPAA governance rules...")
    
    evaluation = evaluate_access_request(args.request, api_key)

    print("\n" + "="*60)
    print("=== SAAS ACCESS RISK EVALUATION REPORT ===")
    print("="*60)
    print(f"Target App:                {evaluation.get('app_name')}")
    print(f"Risk Level:                {evaluation.get('risk_score')}")
    print(f"PHI/PII Hazard Detected:   {evaluation.get('phi_pii_risk')}")
    print(f"BAA Agreement Required:   {evaluation.get('baa_required')}")
    print(f"SSO Enforcement Mandate:   {evaluation.get('sso_enforcement_required')}")
    print(f"Decision Routing:          {evaluation.get('approval_status')}")
    print(f"Governance Rationale:      {evaluation.get('justification')}")
    print("Recommended Controls:")
    for ctrl in evaluation.get("recommended_security_controls", []):
        print(f"  - {ctrl}")
    print("="*60 + "\n")

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(evaluation, f, indent=2)
        print(f"[+] Risk report written to {args.output}")

if __name__ == "__main__":
    main()
