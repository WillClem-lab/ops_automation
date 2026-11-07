#!/usr/bin/env python3
"""
Governed ATS Job Ingestion & Deduplication Engine
Document ID: AGENT-ATS-005
Owner: IT Operations & AI Governance
"""

import os
import sys
import json
import re
from typing import List, Dict, Any

STATE_FILE = "ai-governance/workflows/ats_scraper/seen_jobs.json"

TARGET_KEYWORDS = re.compile(
    r"\b(systems admin|system administrator|it manager|it lead|infrastructure|cloud engineer|"
    r"security engineer|systems engineer|it operations|devops|mcp|n8n)\b", 
    re.IGNORECASE
)

EXCLUSION_KEYWORDS = re.compile(
    r"\b(active secret clearance|top secret/sci|ts/sci)\b", 
    re.IGNORECASE
)

def load_seen_jobs() -> set:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_seen_jobs(seen_ids: set):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen_ids), f, indent=2)

def filter_jobs(raw_jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen_ids = load_seen_jobs()
    matched_jobs = []

    for job in raw_jobs:
        job_id = str(job.get("id") or job.get("job_id"))
        if not job_id or job_id in seen_ids:
            continue

        title = job.get("title", "")
        description = job.get("content", "") or job.get("description", "")

        if EXCLUSION_KEYWORDS.search(description):
            continue

        if TARGET_KEYWORDS.search(title) or TARGET_KEYWORDS.search(description):
            seen_ids.add(job_id)
            matched_jobs.append({
                "job_id": job_id,
                "title": title,
                "company": job.get("company", "Unknown"),
                "location": job.get("location", {}).get("name") if isinstance(job.get("location"), dict) else job.get("location", "Remote"),
                "url": job.get("absolute_url") or job.get("hostedUrl") or job.get("url"),
                "raw_text": description[:3000]
            })

    save_seen_jobs(seen_ids)
    return matched_jobs

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
        results = filter_jobs(data)
        print(json.dumps(results, indent=2))
