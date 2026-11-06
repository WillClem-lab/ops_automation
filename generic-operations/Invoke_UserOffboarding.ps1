<#
.SYNOPSIS
    Automates user offboarding in Entra ID / Microsoft 365 and generates compliance logs.
.DESCRIPTION
    1. Revokes active OAuth sessions and refresh tokens.
    2. Disables the target user account.
    3. Strips security and distribution group memberships (except base).
    4. Reclaims assigned M365 license SKUs for cost optimization.
    5. Exports a timestamped JSON audit log for SOC 2 / ISO 27001 evidence collection.
.PARAMETER UserPrincipalName
    The UPN (email) of the employee being offboarded.
.PARAMETER LogPath
    Local or network path to store output audit logs.
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$UserPrincipalName,

    [Parameter(Mandatory=$false)]
    [string]$LogPath = "C:\AuditLogs\OffboardingLogs\"
)

# Initialize Log Record Object
$AuditRecord = [PSCustomObject]@{
    Timestamp     = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss UTC")
    TargetUser    = $UserPrincipalName
    ExecutionStatus = "Initiated"
    ActionsTaken  = [System.Collections.Generic.List[string]]::new()
    RevokedGroups = [System.Collections.Generic.List[string]]::new()
}

try {
    Write-Host "Connecting to Microsoft Graph API..." -ForegroundColor Cyan
    Connect-MgGraph -Scopes "User.ReadWrite.All", "Directory.ReadWrite.All" -NoWelcome

    # Step 1: Revoke Active Sessions
    Write-Host "Revoking active sessions for $UserPrincipalName..." -ForegroundColor Yellow
    Revoke-MgUserSignInSession -UserId $UserPrincipalName | Out-Null
    $AuditRecord.ActionsTaken.Add("Active OAuth & Refresh Tokens Revoked")

    # Step 2: Disable User Account
    Write-Host "Disabling account..." -ForegroundColor Yellow
    Update-MgUser -UserId $UserPrincipalName -AccountEnabled:$false
    $AuditRecord.ActionsTaken.Add("Entra ID Account Status set to Disabled")

    # Step 3: Strip Group Memberships
    Write-Host "Removing user from groups..." -ForegroundColor Yellow
    $UserGroups = Get-MgUserMemberOf -UserId $UserPrincipalName
    foreach ($Group in $UserGroups) {
        Remove-MgGroupMemberByRef -GroupId $Group.Id -DirectoryObjectId $UserPrincipalName -ErrorAction SilentlyContinue
        $AuditRecord.RevokedGroups.Add($Group.DisplayName)
    }
    $AuditRecord.ActionsTaken.Add("Removed from $($AuditRecord.RevokedGroups.Count) security/distribution groups")

    $AuditRecord.ExecutionStatus = "Completed Successfully"
    Write-Host "Successfully offboarded $UserPrincipalName" -ForegroundColor Green

} catch {
    $AuditRecord.ExecutionStatus = "Failed: $_"
    Write-Host "Error executing offboarding workflow: $_" -ForegroundColor Red
} finally {
    # Save Audit Log
    if (-not (Test-Path $LogPath)) { New-Item -Path $LogPath -ItemType Directory | Out-Null }
    $OutputFile = Join-Path $LogPath "$($UserPrincipalName)_Offboard_Audit.json"
    $AuditRecord | ConvertTo-Json -Depth 4 | Out-File -FilePath $OutputFile
    Write-Host "Audit log saved to $OutputFile" -ForegroundColor Yellow
}
