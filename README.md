# Enterprise IT Operations & Compliance Automation Toolkit

A production-ready automation and governance toolkit engineered for lean IT operations, remote workforce management, and enterprise identity governance across Microsoft 365, Entra ID, and endpoint fleets. 

Designed to eliminate manual administrative overhead, enforce zero-trust security baselines, and generate audit-ready compliance evidence.

---

## 🛠️ General IT Operations & Infrastructure (`/generic-operations/`)

### 1. Automated User Lifecycle & Offboarding (`/generic-operations/Invoke-UserOffboarding.ps1`)
* **Purpose:** One-click offboarding script utilizing Microsoft Graph API.
* **Key Functions:** Revokes active OAuth sessions/tokens, disables Entra ID accounts, removes dynamic/static security groups, and reclaims M365 license SKUs.
* **Operational Impact:** Eliminates manual offboarding gaps and prevents unauthorized access creep.

### 2. Fleet Endpoint Compliance Auditor (`/generic-operations/Get-EndpointComplianceStatus.ps1`)
* **Purpose:** PowerShell auditing tool for hybrid and remote endpoint management (Intune / Action1).
* **Key Functions:** Verifies BitLocker disk encryption, real-time Defender antivirus protection, and OS patch compliance.
* **Operational Impact:** Delivers instant security baseline visibility across remote endpoints.

### 3. CSV Ingestion Example (`/generic-operations/examples/sample_users.csv`)
* **Purpose:** Sanitized user dataset for testing batch user administration workflows.

---

## 🏥 Healthcare & Regulated Environment (`/healthcare-compliance/`)

Specialized technical controls and evidence collectors tailored for **HIPAA-regulated environments, healthtech startups, and clinical infrastructure**.

### 1. HIPAA PHI Access Review & Audit Logger (`/healthcare-compliance/Invoke-HIPAAAccessAudit.ps1`)
* Verifies account disablement and session revocation for users handling Protected Health Information (PHI).
* Generates immutable, timestamped JSON/CSV audit evidence mapped to HIPAA Security Rule (§ 164.312) and SOC 2 requirements.

---

## 📄 Operational Documentation & Governance Policies (`/docs/`)

* **[Standard Operating Procedure: Emergency User Access Revocation (`docs/SOP_Runbook_Template.md`)](docs/SOP_Runbook_Template.md):** Standardized, step-by-step IT runbook for emergency deprovisioning, device isolation, and audit sign-off.
* **[SaaS Governance & Shadow IT Policy (`docs/SaaS_Governance_Policy.md`)](docs/SaaS_Governance_Policy.md):** Operational framework for Single Sign-On (SSO) enforcement, third-party OAuth app triage, and Business Associate Agreement (BAA) requirements.

---

## 📋 Compliance & Regulatory Framework Alignment

| Framework / Standard | Control Scope | Toolkit Asset |
| :--- | :--- | :--- |
| **SOC 2 (Trust Services Criteria)** | Logical Access & Timely Deprovisioning (CC6.1, CC6.2, CC6.3) | `Invoke-UserOffboarding.ps1`, `SOP_Runbook_Template.md` |
| **HIPAA Security Rule** | Access Control (§ 164.312(a)(1)) & Audit Controls (§ 164.312(b)) | `Invoke-HIPAAAccessAudit.ps1`, `SaaS_Governance_Policy.md` |
| **NIST RMF / SP 800-53** | Access Control (AC-2, AC-6) & Flaw Remediation (SI-2) | `Get-EndpointComplianceStatus.ps1` |
| **ISO 27001** | User Access Management (A.9.2) & Endpoint Security (A.11.2) | `enterprise-it-ops-automation` |

---

## 👨‍💻 Author
**William H. Clemons III** — Systems Administrator & IT Infrastructure Lead  
* **Certifications:** CompTIA Security+, CompTIA CSIS, CompTIA Network+, CompTIA A+, ITIL 4 Foundation, NIST RMF Certificate  
* **Contact:** wclemons3@outlook.com | [LinkedIn Profile](https://www.linkedin.com/in/william-clemons-iii)
