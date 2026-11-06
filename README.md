# Enterprise IT Operations & Compliance Automation Toolkit

A production-ready automation toolkit engineered for lean IT operations, remote workforce management, and enterprise identity governance across Microsoft 365, Entra ID, and endpoint fleets.

Designed to eliminate manual administrative overhead, enforce zero-trust security baselines, and automate audit evidence collection.

---

## 🛠️ General IT Operations & Infrastructure Modules

### 1. Automated User Lifecycle & Offboarding (`/generic-operations/Invoke-UserOffboarding.ps1`)
* **Purpose:** One-click offboarding script utilizing Microsoft Graph API.
* **Key Functions:** Revokes active OAuth sessions, disables Entra ID accounts, reclaims unassigned licenses, and removes dynamic/static security groups.
* **Operational Impact:** Eliminates manual offboarding gaps and prevents "access creep."

### 2. Fleet Endpoint Compliance Auditor (`/generic-operations/Get-EndpointCompliance.ps1`)
* **Purpose:** PowerShell auditing tool for hybrid and remote endpoint management (Intune / Action1).
* **Key Functions:** Verifies BitLocker/FileVault encryption status, confirms real-time antivirus protection, and checks OS patch windows.
* **Operational Impact:** Produces instant compliance summaries for remote hardware without manual end-user disruption.

### 3. SaaS License & Shadow IT Triage (`/generic-operations/Get-SaaSLicenseAudit.py`)
* **Purpose:** Python utility to analyze user activity logs across Microsoft 365 and Google Workspace.
* **Key Functions:** Flags inactive users (>30 days) for license reclamation and inventories third-party OAuth app consents.
* **Operational Impact:** Controls SaaS spend and mitigates unapproved SaaS integration risks.

---

## 🏥 Healthcare & Regulated Environment Subsection (`/healthcare-compliance/`)

This dedicated subsection highlights specialized technical controls tailored for **HIPAA-regulated environments, healthtech startups, and clinical infrastructure**.

### 1. HIPAA PHI Access Review & Offboarding Logger (`/healthcare-compliance/Invoke-HIPAAAccessAudit.ps1`)
* Automates mandatory access revocation for users handling Protected Health Information (PHI).
* Generates immutable, timestamped JSON/CSV audit logs for SOC 2 (CC6.1/CC6.3) and HIPAA Security Rule (§ 164.312) evidence collection.

### 2. Business Associate Agreement (BAA) & SaaS Checker (`/healthcare-compliance/Check-BAA-SaaSGovernance.py`)
* Cross-references active cloud tools against an internal inventory of signed BAAs.
* Flags unauthorized cloud storage or messaging tools that could expose PHI.

---

## 📋 Security & Regulatory Framework Alignment

| Framework / Standard | Control Scope | Script Alignment |
| :--- | :--- | :--- |
| **SOC 2 (Trust Services Criteria)** | Logical Access & Timely Deprovisioning (CC6.1, CC6.2) | `Invoke-UserOffboarding.ps1` |
| **NIST RMF / SP 800-53** | Access Control (AC-2, AC-6) & Flaw Remediation (SI-2) | `Get-EndpointCompliance.ps1` |
| **HIPAA Security Rule** | Access Control (§ 164.312(a)(1)) & Audit Controls (§ 164.312(b)) | `/healthcare-compliance/*` |
| **ISO 27001** | User Access Management (A.9.2) & Endpoint Security (A.11.2) | `enterprise-it-ops-automation` |

---

## 👨‍💻 About the Author
**William H. Clemons III** — Systems Administrator & IT Infrastructure Lead with 18+ years of experience leading sole-resource IT operations, endpoint management, and compliance readiness across healthcare, enterprise, and multi-client environments.
* **Certifications:** CompTIA Security+, CompTIA CSIS, CompTIA Network+, CompTIA A+, ITIL 4 Foundation, NIST RMF Certificate
* **Contact:** wclemons3@outlook.com | [LinkedIn Profile](https://www.linkedin.com/in/william-clemons-iii)
