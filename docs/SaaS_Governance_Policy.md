# Enterprise SaaS Governance & Shadow IT Policy

**Document ID:** POL-IT-002  
**Version:** 1.0  
**Effective Date:** October 2026  
**Scope:** Global Enterprise Operations  

---

## 1. Objective
To maintain data privacy, control SaaS expenditure, and ensure all cloud software handling enterprise data meets organizational security baselines and regulatory requirements (SOC 2, ISO 27001, HIPAA).

## 2. Core Governance Rules

### Rule A: Single Sign-On (SSO) & Centralized Identity Mandate
* Any enterprise application supporting SAML 2.0 or OIDC **must** be integrated into the central Identity Provider (Entra ID / Okta).
* Individual local password creation for corporate software is strictly prohibited where SSO is technically supported.

### Rule B: Shadow IT & OAuth Application Triage
* Unsanctioned third-party browser extensions, OAuth consents, or cloud tool sign-ups discovered via discovery tooling (e.g., Torii / Action1) will be triaged within 5 business days:
  1. **Sanction:** Approve, assign business owner, and bring under central SSO/SCIM provisioning.
  2. **Replace:** Transition users to existing, approved enterprise tools.
  3. **Revoke:** Terminate OAuth consent and block access via secure web gateways.

### Rule C: Healthcare & Regulated Data Controls
* No software or cloud platform handling Protected Health Information (PHI) or Sensitive PII may be deployed without an executed **Business Associate Agreement (BAA)** or formal vendor security review on file.

---

## 3. Software Request & Approval Workflow
```text
User Request (Ticket Catalog) 
   └── Initial Technical / SAML Review (IT Ops)
          └── Security & BAA Review (CISO / Security Lead)
                 └── Approval & SSO/SCIM Deployment
