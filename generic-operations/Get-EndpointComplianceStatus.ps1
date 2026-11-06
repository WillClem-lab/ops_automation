<#
.SYNOPSIS
    Queries endpoint security baseline and patch status for Windows machines.
.DESCRIPTION
    Checks BitLocker disk encryption, real-time Defender protection status, and OS build compliance.
    Can be deployed via Intune, Action1, or RMM agent scripts.
#>

function Get-EndpointComplianceStatus {
    [CmdletBinding()]
    param()

    # Query BitLocker Status
    $BitLocker = Get-BitLockerVolume -MountPoint "C:" -ErrorAction SilentlyContinue
    $IsEncrypted = ($BitLocker.ProtectionStatus -eq "On") -and ($BitLocker.VolumeStatus -eq "FullyEncrypted")

    # Query Defender Antivirus Status
    $Defender = Get-MpComputerStatus -ErrorAction SilentlyContinue
    $IsAVActive = $Defender.RealTimeProtectionEnabled

    # Query OS Details
    $OSInfo = Get-CimInstance Win32_OperatingSystem

    # Output Structured Status Object
    [PSCustomObject]@{
        Hostname            = $env:COMPUTERNAME
        OperatingSystem     = $OSInfo.Caption
        OSVersion           = $OSInfo.Version
        BitLockerEncrypted  = $IsEncrypted
        RealTimeAVActive    = $IsAVActive
        AVSignatureDate     = $Defender.AntivirusSignatureLastUpdated
        ZeroTrustCompliant  = ($IsEncrypted -and $IsAVActive)
    }
}

Get-EndpointComplianceStatus | Format-Table -AutoSize
