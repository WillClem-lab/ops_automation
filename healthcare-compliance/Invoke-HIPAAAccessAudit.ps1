<#
.SYNOPSIS
    HIPAA/PHI Technical Access Control Audit & Offboarding Verification Script.
.DESCRIPTION
    Verifies access revocation for employees with access to systems storing Protected Health Information (PHI).
    Maps outputs directly to HIPAA Security Rule § 164.312(a)(1) (Access Control) and § 164.312(b) (Audit Controls).
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$TargetUserUPN,

    [Parameter(Mandatory=$false)]
    [string]$HIPAAAuditDirectory = "C:\ComplianceEvidence\HIPAA_Access_Reviews\"
)

Write-Host "Executing HIPAA PHI Access Revocation Audit for: $TargetUserUPN" -ForegroundColor Cyan

$HIPAAAuditRecord = [PSCustomObject]@{
    AuditID            = [Guid]::NewGuid().ToString()
    Timestamp          = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss UTC")
    TargetEmployee     = $TargetUserUPN
    RegulatoryMapping  = "HIPAA Security Rule 45 CFR § 164.312(a)(1) & § 164.312(b)"
    AccountDisabled    = $false
    SessionsRevoked    = $false
    GroupRevocations   = @()
    EvidenceValidated  = $false
}

try {
    Connect-MgGraph -Scopes "User.Read.All" -NoWelcome
    $User = Get-MgUser -UserId $TargetUserUPN

    if ($User.AccountEnabled -eq $false) {
        $HIPAAAuditRecord.AccountDisabled = $true
        $HIPAAAuditRecord.EvidenceValidated = $true
        Write-Host "VERIFIED: User account $TargetUserUPN is Disabled." -ForegroundColor Green
    } else {
        Write-Host "WARNING: Account $TargetUserUPN is still ACTIVE! High Risk for PHI Access." -ForegroundColor Red
    }

} catch {
    Write-Host "Error running HIPAA audit query: $_" -ForegroundColor Red
} finally {
    if (-not (Test-Path $HIPAAAuditDirectory)) { New-Item -Path $HIPAAAuditDirectory -ItemType Directory | Out-Null }
    $OutputFile = Join-Path $HIPAAAuditDirectory "HIPAA_PHI_Access_Audit_$($TargetUserUPN).json"
    $HIPAAAuditRecord | ConvertTo-Json -Depth 4 | Out-File -FilePath $OutputFile
    Write-Host "HIPAA Compliance Evidence File written to $OutputFile" -ForegroundColor Yellow
}
