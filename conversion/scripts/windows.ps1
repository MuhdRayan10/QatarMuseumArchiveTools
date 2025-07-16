<#  FFmpeg + REDCINE-X PRO bootstrapper (idempotent for FFmpeg)
    Run from an *elevated* PowerShell window.
#>

$ErrorActionPreference = 'Stop'
if (-not ( [Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()
      ).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    Write-Warning 'Re-run this script from an *elevated* PowerShell prompt.'
    exit 1
}

[Net.ServicePointManager]::SecurityProtocol = 3072  # TLS 1.2+

# -------- CONFIG --------
$ffmpegUrl      = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
$ffmpegZip      = "$env:TEMP\ffmpeg.zip"
$ffmpegRoot     = 'C:\Tools\ffmpeg'        # change if desired
$ffmpegBinGlob  = "$ffmpegRoot\ffmpeg-*\bin\ffmpeg.exe"   # wildcard for version folder

$redcineUrl     = 'https://downloads.red.com/software/rcx/win/release/64.0.25/REDCINE-X_PRO_Build_64.0.25.msi'
$redMsi         = "$env:TEMP\REDCINE-X_PRO.msi"
$redProgramDir  = 'C:\Program Files\REDCINE-X PRO 64-bit'
# ------------------------

# ========== FFmpeg ==========
if (Test-Path $ffmpegBinGlob) {
    Write-Host "FFmpeg already present - skipping download/extract."
    $ffmpegResolvedBin = (Get-Item $ffmpegBinGlob | Select-Object -First 1).DirectoryName
} else {
    Write-Host "`nDownloading FFmpeg"
    Invoke-WebRequest $ffmpegUrl -OutFile $ffmpegZip

    Write-Host "Extracting to $ffmpegRoot"
    New-Item $ffmpegRoot -ItemType Directory -Force | Out-Null
    Expand-Archive -Path $ffmpegZip -DestinationPath $ffmpegRoot -Force
    Remove-Item $ffmpegZip

    $ffmpegResolvedBin = (Get-Item $ffmpegBinGlob | Select-Object -First 1).DirectoryName
}

# Add FFmpeg bin to machine PATH if needed
$machinePath = [Environment]::GetEnvironmentVariable('Path','Machine')
if (-not ($machinePath -split ';' | Where-Object { $_ -ieq $ffmpegResolvedBin })) {
    [Environment]::SetEnvironmentVariable('Path', "$machinePath;$ffmpegResolvedBin", 'Machine')
    Write-Host "Added FFmpeg to PATH"
} else {
    Write-Host "FFmpeg already on PATH"
}

# ========== REDCINE-X PRO ==========
if (Test-Path "$redProgramDir\REDline.exe") {
    Write-Host "`nREDCINE-X PRO already present - skipping download/install."
}
else {
    Write-Host "`nDownloading REDCINE-X PRO MSI"
    Invoke-WebRequest $redcineUrl -OutFile $redMsi

    Write-Host "Installing REDCINE-X PRO (silent)"
    Start-Process "msiexec.exe" -ArgumentList "/i `"$redMsi`" /qn /norestart" -Wait
    Remove-Item $redMsi
}

# ---------- Make sure libmmd.dll is available ----------
$libNeeded   = Join-Path $redProgramDir 'libmmd.dll'

if (-not (Test-Path $libNeeded)) {
    # 1) try to copy an existing Intel DLL 
    $dllSource = Get-ChildItem 'C:\Program Files*\Intel*' -Recurse -Filter libmmd.dll `
                   -ErrorAction SilentlyContinue | Select-Object -First 1

    if ($dllSource) {
        Copy-Item $dllSource.FullName $libNeeded -Force
        Write-Host "Copied libmmd.dll from $($dllSource.DirectoryName)"
    }
    else {
        # 2) fall back to downloading Intel’s runtime
        Write-Warning "libmmd.dll still missing—installing Intel compiler runtime..."

        $intelUrl  = 'https://registrationcenter-download.intel.com/akdlm/IRC_NAS/7f810440-2a66-4d34-b05f-8f4395667844/w_dpcpp_cpp_runtime_p_2025.1.1.1001.exe'
        $intelExe  = "$env:TEMP\intel_cpp_runtime.exe"

        Invoke-WebRequest $intelUrl -OutFile $intelExe
        Start-Process $intelExe -ArgumentList '--silent' -Wait
        Remove-Item $intelExe

        if (-not (Test-Path $libNeeded)) {
            Write-Warning "Intel runtime installed but libmmd.dll still not found—check manually."
        } else {
            Write-Host "Intel runtime installed; libmmd.dll resolved."
        }
    }
}


# Add REDline (CLI) folder to PATH if needed
if (Test-Path "$redProgramDir\REDline.exe") {
    $machinePath = [Environment]::GetEnvironmentVariable('Path','Machine')
    if (-not ($machinePath -split ';' | Where-Object { $_ -ieq $redProgramDir })) {
        [Environment]::SetEnvironmentVariable('Path', "$machinePath;$redProgramDir", 'Machine')
        Write-Host "Added Redline to PATH"
    } else {
        Write-Host "Redline already on PATH"
    }
} else {
    Write-Warning "REDline.exe not found in $redProgramDir — adjust if you installed RCX elsewhere."
}

Write-Host "`nAll done!  Open a *new* terminal (or reboot) so the updated PATH takes effect."
