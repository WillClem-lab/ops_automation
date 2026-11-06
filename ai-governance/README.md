
# AI Governance & Governed Automation Module (`/ai-governance/`)

This directory contains operational frameworks, data protection baselines, and production-ready workflow definitions for administering generative AI tools, Large Language Model (LLM) integrations, and autonomous agents in enterprise environments.

---

## Module Components

1. **`AI_Acceptable_Use_Policy.md`:**  
   Formal governance policy establishing data classification boundaries, approved tool catalogs (Claude, Notion AI), LLM training opt-outs, Zero Data Retention (ZDR) baselines, and PHI/PII prompt prohibitions.

2. **`n8n_Ticket_Triage_Workflow.json`:**  
   Exportable n8n workflow definition illustrating an AI-assisted IT helpdesk triage engine with built-in Human-in-the-Loop (HITL) Slack approval prompts and JSON audit logging.

---

## Governed Architecture Principles

* **Zero-Trust AI Scoping:** AI agents and LLM API nodes operate under least-privilege API credentials.
* **Human-in-the-Loop Checkpoint:** No automated action altering user entitlements or endpoint states occurs without explicit administrative authorization.
* **Data Boundary Protection:** Strictly enforces guardrails ensuring Protected Health Information (PHI), PII, administrative credentials, and proprietary code are excluded from model context windows.
* **Audit Transparency:** All automated classification outputs and admin approvals generate immutable audit logs to satisfy SOC 2 (CC6.1) and HIPAA (§ 164.312) controls.

---

## How to Import the n8n Workflow

1. Open your self-hosted **n8n** administrative console.
2. Click **Workflows** -> **Import from File**.
3. Select `n8n_Ticket_Triage_Workflow.json`.
4. Configure your OpenAI / Anthropic API credentials and Slack webhook channel variables.
