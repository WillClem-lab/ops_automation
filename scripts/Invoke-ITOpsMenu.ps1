<#
.SYNOPSIS
    Interactive CLI menu for executing IT Operations & Compliance Toolkit scripts.
#>

function Show-Menu {
    Clear-Host
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host "       ENTERPRISE IT OPS AUTOMATION TOOLKIT         " -ForegroundColor Cyan
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host "1. Execute User Offboarding & Revocation (M365)"
    Write-Host "2. Audit Local Endpoint Compliance (BitLocker/AV)"
    Write-Host "3. Run HIPAA Access Review Audit"
    Write-Host "Q. Quit"
    Write-Host "====================================================" -ForegroundColor Cyan
}

do {
    Show-Menu
    $selection = Read-Host "Select an option"
    switch ($selection) {
        '1' { Write-Host "Running Offboarding Script..."; & ".\generic-operations\Invoke-UserOffboarding.ps1" }
        '2' { Write-Host "Auditing Endpoint..."; & ".\generic-operations\Get-EndpointComplianceStatus.ps1" }
        '3' { Write-Host "Executing HIPAA Audit..."; & ".\healthcare-compliance\Invoke-HIPAAAccessAudit.ps1" }
        'Q' { Write-Host "Exiting toolkit..." -ForegroundColor Yellow }
        default { Write-Host "Invalid selection." -ForegroundColor Red }
    }
    if ($selection -ne 'Q') { Pause }
} until ($selection -eq 'Q')
