# Standard Operating Procedure: Remediation of Stale Entra ID OAuth Tokens and Expired Conditional Access Sessions
**Document ID:** SOP-AUTO-IAM-4109
**Version:** 1.0
**Compliance Mapping:** SOC 2 (CC6.1, CC6.8), NIST RMF (AC-2, SI-2)

---

## 1. Executive Summary & Trigger Condition
This Standard Operating Procedure (SOP) defines the operational workflow for resolving client-side authentication failures caused by desynchronization between Microsoft Entra ID session controls and locally cached OAuth tokens. 

**Trigger Condition:**
* A user experiences repeated `HTTP 401 Unauthorized` errors when connecting to Microsoft Entra ID resources or Microsoft 365 cloud workloads.
* Client sign-in attempts fail continuously from a known network endpoint (`<CLIENT_IP>`) despite entering valid credentials.
* Conditional Access session logs indicate token revocation, but the local device persists an invalid or expired OAuth refresh token.

## 2. Environment & Affected Systems
* **Identity Provider:** Microsoft Entra ID (Azure AD)
* **Client Operating System:** Windows 10 / Windows 11 Enterprise
* **Client Components:** Windows Credential Manager, Web Account Manager (WAM)
* **Administrative Tools:** Microsoft Graph PowerShell SDK (`Microsoft.Graph.Users`)
* **Impacted Endpoints:** Workstations accessing corporate cloud services from `<CLIENT_IP>`

## 3. Root Cause Analysis (RCA)
A discrepancy between server-side session validity and client-side credential caching generates the failure:
1. **Server-Side Session Invalidation:** An Entra ID Conditional Access policy expires the user session or revokes the server-side refresh token based on policy thresholds (e.g., session timeout, network transition, or risk detection).
2. **Local Token Persistence:** The client workstation fails to clear the now-invalid OAuth refresh token stored locally in the Windows Credential Manager and local identity cache.
3. **Authentication Deadlock:** The client application continuously presents the cached, stale refresh token during authentication attempts instead of initiating a full interactive re-authentication prompt. Entra ID rejects the request with an `HTTP 401 Unauthorized` status code.

## 4. Step-by-Step Remediation Workflow

### Step 1: Revoke User Sessions in Microsoft Entra ID
Administrators must invalidate all active refresh tokens and sessions for the affected user to force a clean authentication state in the identity provider.

1. Open PowerShell with administrative privileges and connect to Microsoft Graph:
   ```powershell
   Connect-MgGraph -Scopes "User.ReadWrite.All"
   ```

2. Revoke the active sign-in sessions for the target identity:
   ```powershell
   Revoke-MgUserSignInSession -UserId "<TARGET_USER_UPN>"
   ```
   *Example: `Revoke-MgUserSignInSession -UserId "john.doe@example.com"`*

3. Confirm command execution returns `True`.

### Step 2: Purge Cached Credentials on the Endpoint
Purge the stale refresh tokens from the user's local operating system profile.

1. Instruct the user to close all open Microsoft 365 applications, browsers, and Teams sessions.
2. Open a Command Prompt or PowerShell terminal in the user's session.
3. Query and delete cached Microsoft/Office generic credentials:
   ```cmd
   cmdkey /list | findstr /i "Microsoft Office"
   ```
4. For each relevant credential found (e.g., `MicrosoftOffice16_Data:...`), delete it manually or execute:
   ```powershell
   # Enumerate and clear Office/Entra ID generic credentials
   cmdkey /list | ForEach-Object {
       if ($_ -match "Target:\s+(MicrosoftOffice\S+|msteams\S+|AzureAD\S+)") {
           $target = $matches[1]
           cmdkey /delete:$target
       }
   }
   ```
5. Navigate to **Windows Settings > Accounts > Access work or school**, select the account, and verify if a "Fix account" prompt appears.

### Step 3: Clear Browser and WAM Authentication Cache (If Applicable)
If issues persist within web browsers or modern apps:
1. Clear cookies and cached data for `login.microsoftonline.com`.
2. Clear the Web Account Manager (WAM) token cache folder:
   ```powershell
   Remove-Item -Path "$env:LOCALAPPDATA\Packages\Microsoft.AAD.BrokerPlugin_cw5n1h2txyewy\AC\TokenBroker\Accounts\*" -Force -Recurse -ErrorAction SilentlyContinue
   ```

### Step 4: Re-Authentication and Verification
1. Instruct the user to reboot the device or restart the impacted applications.
2. Direct the user to navigate to `https://myapplications.microsoft.com`.
3. Complete the interactive authentication challenge, including Multi-Factor Authentication (MFA).
4. Review Entra ID Sign-In Logs for the user:
   * Navigate to **Entra Admin Center > Monitoring & health > Sign-in logs**.
   * Verify that the latest sign-in record indicates **Success (Status 0)**.

## 5. Prevention & Hardening Measures
* **Continuous Access Evaluation (CAE):** Ensure Continuous Access Evaluation is enabled across Entra ID tenant settings to allow real-time token revocation and auto-recovery between applications and the identity provider.
* **Conditional Access Session Controls:** Review Conditional Access Sign-In Frequency (SIF) configurations to prevent aggressive token timeouts that conflict with native OS token broker refresh cycles.
* **Endpoint Management (Intune):** Deploy configuration profiles to manage Enterprise State Roaming and ensure the Microsoft Entra broker plugin (`Microsoft.AAD.BrokerPlugin`) is maintained and operational on all managed endpoints.
* **Monitoring and Alerting:** Configure automated alerts in Microsoft Sentinel or Defender for Cloud Apps for high-volume 401/403 authorization failures originating from specific user accounts.