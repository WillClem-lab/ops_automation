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
1. Open an Administrative PowerShell Console and execute the offboarding automation script:
   ```powershell
   .\generic-operations\Invoke-UserOffboarding.ps1 -UserPrincipalName "target.user@domain.com"

Verify that active OAuth refresh tokens and Entra ID web sessions have been forcibly invalidated.

Confirm account status is toggled to Disabled.

Step 2: Access Group & License Reclamation
Remove user from all dynamic and static security groups, excluding base retention groups.

Unassign Microsoft 365 / SaaS license SKUs to return licenses to the available pool.

Step 3: Remote Endpoint Lock & Wipe
Log into MDM Portal (Intune / Action1 / Kandji).

Issue Remote Lock or Initiate Remote Wipe for assigned hardware.

Verify BitLocker / FileVault device key escrow is secured for asset recovery.

Step 4: Audit Trail Log Verification
Confirm the timestamped audit log was generated at: C:\AuditLogs\OffboardingLogs\<UPN>_Offboard_Audit.json.

Attach the generated JSON log to the offboarding ticket in the ticketing platform.

5. Verification & Sign-off
Incident / Task Lead: William H. Clemons III

Verification Checklist:

[ ] Session tokens revoked

[ ] Entra ID account disabled

[ ] Licenses unassigned

[ ] Audit log attached to ticket
