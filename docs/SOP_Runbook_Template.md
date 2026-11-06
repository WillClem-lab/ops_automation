# Standard Operating Procedure (SOP): Emergency User Access Revocation & Deprovisioning

**Document ID:** SOP-IT-004  
**Version:** 1.2  
**Effective Date:** October 2026  
**Owner:** IT Infrastructure & Operations  
**Compliance Standards:** SOC 2 (CC6.1, CC6.3), HIPAA Security Rule (§ 164.312), NIST RMF (AC-2)  

---

## 1. Purpose
This procedure defines the mandatory execution sequence for performing emergency or immediate account deprovisioning and credential revocation across enterprise identity providers, SaaS platforms, and endpoint hardware.

## 2. Scope
Applies to all full-time employees, contractors, third-party vendors, and seasonal personnel across Microsoft 365, Entra ID, Google Workspace, and connected SaaS applications.

## 3. Trigger Conditions
* Notification from HR / Legal regarding immediate termination or involuntary separation.
* Security Operations alert indicating compromised administrative credentials or active account abuse.
* Lost or stolen company-owned mobile device or endpoint handling sensitive data.

## 4. Execution Workflow (Step-by-Step)

### Step 1: Session Termination & Account Suspension
1. Open Administrative PowerShell Console and execute the offboarding automation script:
   ```powershell
   .\generic-operations\Invoke-UserOffboarding.ps1 -UserPrincipalName "target.user@domain.com"
