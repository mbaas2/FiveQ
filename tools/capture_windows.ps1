# Captures the FiveQThoughts main window (light + dark) for the website.
# Untested draft – written on macOS, see SCREENSHOTS-WINDOWS.md.
#
#   powershell -ExecutionPolicy Bypass -File tools\capture_windows.ps1 -Lang de -Exe "$env:LOCALAPPDATA\Programs\FiveQThoughts\FiveQThoughts.exe"
#
# The window is captured with PrintWindow (works even if partly covered) incl. the
# Windows 11 title bar. Output: docs\img\win-<lang>-light.png / win-<lang>-dark.png
param(
    [Parameter(Mandatory = $true)][ValidateSet("de", "en")][string]$Lang,
    [string]$Exe = "$env:LOCALAPPDATA\Programs\FiveQThoughts\FiveQThoughts.exe",
    [string]$Backend = "",   # e.g. http://127.0.0.1:11525 – read from the running app if empty
    [int]$Width = 1180,
    [int]$Height = 840
)

$ErrorActionPreference = "Stop"
$Out = Join-Path (Split-Path $PSScriptRoot -Parent) "docs\img"
New-Item -ItemType Directory -Force $Out | Out-Null

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class W {
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int hh, bool repaint);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
}
"@
[W]::SetProcessDPIAware() | Out-Null

function Get-MainWindow {
    for ($i = 0; $i -lt 40; $i++) {
        $p = Get-Process FiveQThoughts -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
        if ($p) { return $p.MainWindowHandle }
        Start-Sleep -Milliseconds 500
    }
    throw "FiveQThoughts window not found"
}

function Set-Config($theme) {
    if (-not $Backend) { return }
    $body = @{ language = $Lang; theme = $theme; languageOnly = $true } | ConvertTo-Json
    Invoke-RestMethod -Method Post -Uri "$Backend/api/config" -ContentType "application/json" -Body $body | Out-Null
}

foreach ($theme in @("light", "dark")) {
    Set-Config $theme
    Get-Process FiveQThoughts -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 1
    Start-Process $Exe
    $h = Get-MainWindow
    [W]::MoveWindow($h, 80, 80, $Width, $Height, $true) | Out-Null
    [W]::SetForegroundWindow($h) | Out-Null
    Start-Sleep -Seconds 9   # let thoughts and images load

    $r = New-Object W+RECT
    [W]::GetWindowRect($h, [ref]$r) | Out-Null
    $bmp = New-Object System.Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $hdc = $g.GetHdc()
    [W]::PrintWindow($h, $hdc, 2) | Out-Null   # PW_RENDERFULLCONTENT (needed for WebView2)
    $g.ReleaseHdc($hdc); $g.Dispose()
    $file = Join-Path $Out "win-$Lang-$theme.png"
    $bmp.Save($file, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
    Write-Host "captured $file"
}
