# Enterprise IT Operations & Compliance Automation Toolkit

A production-ready automation and governance toolkit engineered for lean IT operations, remote workforce management, governed AI enablement, and enterprise identity governance across Microsoft 365, Entra ID, and endpoint fleets. 

Designed to eliminate manual administrative overhead, enforce zero-trust security baselines, establish AI prompt guardrails, and generate audit-ready compliance evidence.

---

## General IT Operations & Infrastructure (`/generic-operations/`)

### 1. Automated User Lifecycle & Offboarding (`/generic-operations/Invoke-UserOffboarding.ps1`)
* **Purpose:** One-click offboarding script utilizing the Microsoft Graph API.
* **Key Functions:** Revokes active OAuth sessions/tokens, disables Entra ID accounts, removes dynamic/static security groups, and reclaims M365 license SKUs.
* **Operational Impact:** Eliminates manual offboarding gaps and prevents unauthorized access creep.

### 2. Fleet Endpoint Compliance Auditor (`/generic-operations/Get-EndpointComplianceStatus.ps1`)
* **Purpose:** PowerShell auditing tool for hybrid and remote endpoint management (Intune / Action1).
* **Key Functions:** Verifies BitLocker disk encryption, real-time Defender antivirus protection, and OS patch compliance.
* **Operational Impact:** Delivers instant security baseline visibility across remote endpoints.

### 3. CSV Ingestion Example (`/generic-operations/examples/sample_users.csv`)
* **Purpose:** Sanitized user dataset for testing batch user administration workflows.

---

## Governed AI Enablement, Automation, and Autonomous Agents (`/ai-governance/`)

Specialized governance frameworks, data protection guardrails, production-ready Python autonomous agents, and protocol servers engineered for enterprise Large Language Model (LLM) deployment across SOC 2 and HIPAA environments.

### 1. Enterprise AI Acceptable Use Policy (`/ai-governance/AI_Acceptable_Use_Policy.md`)
- **Purpose:** Formal operational framework establishing prompt data boundaries, approved AI tool catalogs (Claude, Notion AI), and vendor Zero-Data-Retention (ZDR) baselines.
- **Key Controls:** Prohibits PHI/PII and credential inputs; mandates SSO/SCIM provisioning and LLM model training opt-outs.

### 2. Governed Helpdesk Triage Workflow (`/ai-governance/n8n_Ticket_Triage_Workflow.json`)
- **Purpose:** Exportable n8n workflow definition utilizing LLM API nodes for automated ticket classification and routing.
- **Key Controls:** Enforces Human-in-the-Loop (HITL) Slack admin approval gates before execution and logs timestamped audit events.

### 3. Automated Knowledge Base & SOP Generator Agent (`/ai-governance/workflows/kb_generator_agent.py`)
- **Purpose:** Autonomous documentation engine that converts raw incident logs and triage notes into standardized Markdown runbooks.
- **Key Controls:** Includes regex-based pre-flight redaction guardrails for PII/PHI, IPv4 addresses, and administrative credentials before invoking the Gemini API (`gemini-3.8-flash`).

### 4. Governed Access Request & Risk Evaluation Agent (`/ai-governance/workflows/saas_access_agent.py`)
- **Purpose:** Risk evaluation engine that parses end-user SaaS access requests against SOC 2 and HIPAA governance matrices.
- **Key Controls:** Detects PHI/PII hazards, mandates BAA requirements and SSO/SCIM enforcement, and generates structured JSON outputs flagging mandatory Human-in-the-Loop (HITL) admin approvals.

### 5. Self-Healing Endpoint Remediation Agent (`/ai-governance/workflows/remediation_agent.py`)
- **Purpose:** Remediation engine that ingests non-compliance JSON logs, diagnoses security gaps (e.g., missing BitLocker encryption), and stages targeted PowerShell remediation payloads.
- **Key Controls:** Enforces HITL authorization gates before executing high-risk administrative actions and appends immutable audit logs (`remediation_audit.log`).

### 6. Enterprise IT Operations Model Context Protocol Server (`/ai-governance/mcp-server/it_ops_mcp_server.py`)
- **Purpose:** FastMCP server exposing local user lifecycle datasets, remediation audit trails, and compliance framework mappings (SOC 2, HIPAA, NIST RMF) over STDIO / JSON-RPC.
- **Key Controls:** Enables LLM assistants (e.g., Claude Desktop, Cursor) to execute secure, read-only queries against local IT telemetry without direct system execution access.

### 7. Module Overview & Integration Guide (`/ai-governance/README.md`)
- **Purpose:** Architectural documentation detailing least-privilege API scoping, HITL checkpoints, and step-by-step n8n import steps.
---

## Healthcare & Regulated Environment (`/healthcare-compliance/`)

Specialized technical controls and evidence collectors tailored for **HIPAA-regulated environments, healthtech startups, and clinical infrastructure**.

### 1. HIPAA PHI Access Review & Audit Logger (`/healthcare-compliance/Invoke-HIPAAAccessAudit.ps1`)
* Verifies account disablement and session revocation for users handling Protected Health Information (PHI).
* Generates immutable, timestamped JSON/CSV audit evidence mapped to HIPAA Security Rule (§ 164.312) and SOC 2 requirements.

---

## Operational Documentation & Governance Policies (`/docs/`)

* **[Standard Operating Procedure: Emergency User Access Revocation (`docs/SOP_Runbook_Template.md`)](docs/SOP_Runbook_Template.md):** Standardized, step-by-step IT runbook for emergency deprovisioning, device isolation, and audit sign-off.
* **[SaaS Governance & Shadow IT Policy (`docs/SaaS_Governance_Policy.md`)](docs/SaaS_Governance_Policy.md):** Operational framework for Single Sign-On (SSO) enforcement, third-party OAuth app triage, and Business Associate Agreement (BAA) requirements.

---

## Compliance & Regulatory Framework Alignment

| Framework / Standard | Control Scope | Toolkit Asset |
| :--- | :--- | :--- |
| **SOC 2 (Trust Services Criteria)** | Logical Access, Timely Deprovisioning, & System Operations (CC6.1, CC6.3, CC6.8) | `Invoke-UserOffboarding.ps1`, `AI_Acceptable_Use_Policy.md`, `SOP_Runbook_Template.md` |
| **HIPAA Security Rule** | Access Control (§ 164.312(a)(1)) & Audit Controls (§ 164.312(b)) | `Invoke-HIPAAAccessAudit.ps1`, `SaaS_Governance_Policy.md`, `AI_Acceptable_Use_Policy.md` |
| **NIST RMF / SP 800-53** | Access Control (AC-2, AC-6), Identification & Auth (IA-2), & Flaw Remediation (SI-2) | `Get-EndpointComplianceStatus.ps1`, `AI_Acceptable_Use_Policy.md` |
| **ISO 27001** | User Access Management (A.9.2), Endpoint Security (A.11.2), & Supplier Relationships (A.15.1) | `enterprise-it-ops-automation`, `n8n_Ticket_Triage_Workflow.json` |

---

## Author
**William H. Clemons III** — Systems Administrator & IT Infrastructure Lead  
* **Certifications:** CompTIA Security+, CompTIA CSIS, CompTIA Network+, CompTIA A+, ITIL 4 Foundation, NIST RMF Certificate  
* **Contact:** wclemons3@outlook.com | [LinkedIn Profile](https://www.linkedin.com/in/william-clemons-iii)
