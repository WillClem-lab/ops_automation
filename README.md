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

## Governed AI Enablement & Automation (`/ai-governance/`)

Specialized governance frameworks, data protection guardrails, and workflow definitions for enterprise Large Language Model (LLM) and autonomous agent deployment.

### 1. Enterprise AI Acceptable Use Policy (`/ai-governance/AI_Acceptable_Use_Policy.md`)
* **Purpose:** Formal operational framework establishing prompt data boundaries, approved AI tool catalogs (Claude, Notion AI), and vendor Zero-Data-Retention (ZDR) baselines.
* **Key Controls:** Prohibits PHI/PII and credential inputs; mandates SSO/SCIM provisioning and LLM model training opt-outs.

### 2. Governed Helpdesk Triage Workflow (`/ai-governance/n8n_Ticket_Triage_Workflow.json`)
* **Purpose:** Exportable n8n workflow definition utilizing LLM API nodes for automated ticket classification and routing.
* **Key Controls:** Enforces Human-in-the-Loop (HITL) Slack admin approval gates before execution and logs timestamped audit events.

### 3. Module Overview & Integration Guide (`/ai-governance/README.md`)
* **Purpose:** Architectural documentation detailing least-privilege API scoping, HITL checkpoints, and step-by-step n8n import steps.

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
