# Enterprise AI Acceptable Use & Data Governance Policy

**Document ID:** POL-IT-003  
**Version:** 1.0  
**Effective Date:** October 2026  
**Owner:** IT Operations & Information Security  
**Compliance Standards:** SOC 2 (CC6.1, CC6.8), HIPAA Security Rule (§ 164.312), NIST RMF (AC-2, IA-2)  

---

## 1. Purpose
This policy establishes mandatory operational guardrails, data boundaries, and entitlement governance for all generative AI models, Large Language Model (LLM) APIs, autonomous agents, and AI-assisted automation tools deployed across enterprise environments.

## 2. Scope
Applies to all full-time personnel, contractors, third-party operators, self-hosted services (e.g., n8n AI nodes), and SaaS platforms featuring integrated AI capabilities (e.g., Claude, Notion AI, OpenAI API).

---

## 3. Data Classification & Prompt Restrictions

### Prohibited Prompt Inputs (Never Allowed)
The following data categories are strictly prohibited from being entered into any public or non-enterprise AI prompt, model context window, or unapproved API endpoint :
* **Protected Health Information (PHI):** Patient records, medical IDs, clinical diagnostic data, or health insurance information.
* **Personally Identifiable Information (PII):** Social Security Numbers, personal banking details, driver's licenses, or home addresses.
* **Administrative Credentials:** API tokens, OAuth refresh tokens, service account keys, private SSH keys, passwords, or database connection strings.
* **Proprietary Source Code & System Configs:** Internal application source code, network topology maps, firewall rulebases, or unannounced product specs.

---

## 4. Approved AI System Catalog & Vendor Requirements

| AI System / Platform | Deployment Model | Approved Use Cases | Required Security Controls |
| :--- | :--- | :--- | :--- |
| **Claude / Anthropic** | Enterprise SSO | Writing assistance, KB drafting, policy reviews | SSO/SCIM provisioning, Zero Data Retention (ZDR), Training Opt-Out enabled  |
| **Notion AI & Agents** | Enterprise Workspace | Workspace indexing, document summaries, project tracking | Scoped Teamspace permissions, Admin AI feature toggles  |
| **n8n AI Workflow Nodes** | Self-Hosted / Scoped API | Ticket categorization, log parsing, automated routing | Scoped API keys, Human-in-the-Loop (HITL) checkpoints  |

---

## 5. Integration Governance & Human-in-the-Loop (HITL)

1. **Least Privilege API Tokens:** All LLM API integrations (OpenAI/Anthropic) must use scoped service credentials stored securely in secret managers (e.g., 1Password, Azure Key Vault) with zero hardcoded keys.
2. **Mandatory Human Approval:** No AI agent or automated workflow may perform destructive identity or infrastructure actions (e.g., disabling accounts, deleting resources, modifying firewall policies) without explicit human administrative approval in Slack/ticketing queues.
3. **Audit Logging:** All automated AI workflow transactions must emit timestamped audit logs containing input prompt metadata, model ID, response status, and administrator approval IDs.

---

## 6. Policy Verification & Compliance

* **Policy Owner:** William H. Clemons III — IT Infrastructure Lead 
* **Review Cycle:** Semi-Annual / Post-Incident Audit Review
