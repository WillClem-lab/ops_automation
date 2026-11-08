#!/usr/bin/env python3
"""
OpenAI Job Fit Scoring & Alignment Engine (Governed)
Document ID: AGENT-ATS-006
Owner: IT Operations & AI Governance
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from dotenv import load_dotenv, find_dotenv

# Traverses parent directories to locate root .env file
load_dotenv(find_dotenv())

PROFILE_PATH = "ai-governance/workflows/ats_scraper/candidate_profile.json"
PROFILE_EXAMPLE_PATH = "ai-governance/workflows/ats_scraper/candidate_profile.json.example"

def get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY") or os.getenv("N8N_INSTANCE_AI_MODEL_API_KEY")
    if not key:
        sys.exit("[ERROR] OPENAI_API_KEY or N8N_INSTANCE_AI_MODEL_API_KEY not found in environment.")
    return key

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

def evaluate_job(job_data: dict, api_key: str, model_name: str) -> dict:
    profile = load_candidate_profile()
    
    system_prompt = f"""You are an Executive IT Recruiter and Candidate Alignment Engine.
Analyze the provided job description against the candidate profile.

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

    user_content = f"Job Title: {job_data.get('title', 'N/A')}\nCompany: {job_data.get('company', 'N/A')}\nJob Description:\n\"\"\"{job_data.get('raw_text', '')}\"\"\""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }

    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            raw_text = res_data["choices"][0]["message"]["content"]
            clean_json = strip_emojis(raw_text)
            parsed = json.loads(clean_json)
            
            # Pass original metadata downstream for n8n alerts
            parsed["title"] = job_data.get("title")
            parsed["company"] = job_data.get("company")
            return parsed
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {
            "error": f"HTTP {e.code}: {error_body}",
            "company": job_data.get("company")
        }
    except Exception as e:
        return {
            "error": f"Evaluation failed: {str(e)}",
            "company": job_data.get("company")
        }

if __name__ == "__main__":
    api_key = get_api_key()
    # Set default model to gpt-6-luna
    model_name = os.getenv("OPENAI_MODEL", "gpt-6-luna")
    
    input_data = None
    
    # 1. Read input from CLI file argument if provided
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            input_data = json.load(f)
    # 2. Read input from n8n stdin stream
    elif not sys.stdin.isatty():
        raw_stdin = sys.stdin.read().strip()
        if raw_stdin:
            input_data = json.loads(raw_stdin)

    if not input_data:
        sys.exit("[ERROR] No input job data provided via file argument or n8n stdin pipe.")

    # 3. Process array of items or single job object
    if isinstance(input_data, list):
        results = [evaluate_job(job, api_key, model_name) for job in input_data]
        print(json.dumps(results, indent=2))
    elif isinstance(input_data, dict):
        eval_result = evaluate_job(input_data, api_key, model_name)
        print(json.dumps(eval_result, indent=2))