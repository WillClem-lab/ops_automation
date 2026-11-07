#!/usr/bin/env python3
"""
Gemini Job Fit Scoring & Alignment Engine (Governed)
Document ID: AGENT-ATS-006
Owner: IT Operations & AI Governance
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error

PROFILE_PATH = "ai-governance/workflows/ats_scraper/candidate_profile.json"
PROFILE_EXAMPLE_PATH = "ai-governance/workflows/ats_scraper/candidate_profile.json.example"

def load_candidate_profile() -> dict:
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    elif os.path.exists(PROFILE_EXAMPLE_PATH):
        with open(PROFILE_EXAMPLE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "experience": "IT Infrastructure & Systems Administration",
        "certifications": ["Security+", "Network+"],
        "core_skills": ["PowerShell", "Python", "Identity Management"]
    }

def strip_emojis(text: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def evaluate_job(job_data: dict, api_key: str) -> dict:
    profile = load_candidate_profile()
    
    system_prompt = f"""You are an Executive IT Recruiter and Candidate Alignment Engine.
Analyze the following job description against the candidate profile provided.

Candidate Profile:
{json.dumps(profile, indent=2)}

Formatting Rules:
- Do NOT use emojis, emoticons, or decorative Unicode symbols in any generated text.
- Enforce clean, standard technical prose and formal JSON output only.

Return ONLY a valid JSON object matching this schema:
{{
  "fit_score": 8,
  "target_salary_found": "string or Not Listed",
  "key_alignment_points": ["string", "string"],
  "potential_gaps": ["string"],
  "outreach_angle": "string"
}}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"{system_prompt}\n\nJob Title: {job_data.get('title')}\nCompany: {job_data.get('company')}\nJob Description:\n\"\"\"{job_data.get('raw_text')}\"\"\""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            clean_json = strip_emojis(raw_text)
            return json.loads(clean_json)
    except Exception as e:
        sys.exit(f"[ERROR] Evaluation failed: {str(e)}")

if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit("[ERROR] GEMINI_API_KEY not set in environment.")
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            job = json.load(f)
        eval_result = evaluate_job(job, api_key)
        print(json.dumps(eval_result, indent=2))
