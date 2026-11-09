# Captures the FiveQThoughts main window (light + dark) for the website.
#
#   powershell -ExecutionPolicy Bypass -File tools\capture_windows.ps1 -Lang de -Exe "$env:LOCALAPPDATA\Programs\FiveQThoughts\FiveQThoughts.exe"
#
# The window is captured with PrintWindow (works even if partly covered) incl. the
# Windows 11 title bar, cropped to DWMWA_EXTENDED_FRAME_BOUNDS.
# Output: docs\img\win-<lang>-light.png / win-<lang>-dark.png
param(
    [Parameter(Mandatory = $true)][ValidateSet("de", "en")][string]$Lang,
    [string]$Exe = "$env:LOCALAPPDATA\Programs\FiveQThoughts\FiveQThoughts.exe",
    [string]$Backend = "",   # unused when writing config.local.json directly
    [int]$Width = 1194,      # 1180 visible px + 2x7px invisible Win11 resize border
    [int]$Height = 865
)

$ErrorActionPreference = "Stop"
$Out = Join-Path (Split-Path $PSScriptRoot -Parent) "docs\img"
New-Item -ItemType Directory -Force $Out | Out-Null

$cfgPath = "$env:APPDATA\FiveQThoughts\config.local.json"
$winPath = "$env:LOCALAPPDATA\FiveQThoughts\window.txt"

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public static class W {
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int hh, bool repaint);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, uint msg, IntPtr wParam, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr hwnd, int dwAttribute, out RECT pvAttribute, int cbAttribute);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  public static IntPtr FindFiveQWindow() {
    IntPtr found = IntPtr.Zero;
    EnumWindows((h, l) => {
      if (!IsWindowVisible(h)) return true;
      var sb = new StringBuilder(256);
      GetWindowText(h, sb, 256);
      if (sb.ToString().StartsWith("FiveQThoughts", StringComparison.Ordinal)) {
        found = h;
        return false;
      }
      return true;
    }, IntPtr.Zero);
    return found;
  }
}
"@
[W]::SetProcessDPIAware() | Out-Null

function Get-MainWindow {
    for ($i = 0; $i -lt 40; $i++) {
        $h = [W]::FindFiveQWindow()
        if ($h -ne [IntPtr]::Zero) { return $h }
        Start-Sleep -Milliseconds 500
    }
    throw "FiveQThoughts window not found"
}

$origLight = (Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize").AppsUseLightTheme

try {
    foreach ($theme in @("light", "dark")) {
        Get-Process FiveQThoughts -ErrorAction SilentlyContinue | Stop-Process -Force
        Get-Process FiveQThoughts-backend -ErrorAction SilentlyContinue | Stop-Process -Force
        Start-Sleep -Seconds 1

        if (Test-Path $cfgPath) {
            $cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
            $cfg.cardCount = 6
            $cfg.language = $Lang
            $cfg.theme = $theme
            [System.IO.File]::WriteAllText($cfgPath, ($cfg | ConvertTo-Json), (New-Object System.Text.UTF8Encoding($false)))
        }
        [System.IO.File]::WriteAllText($winPath, "300,80,$Width,$Height,0", (New-Object System.Text.UTF8Encoding($false)))

        $lightVal = if ($theme -eq "light") { 1 } else { 0 }
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value $lightVal

        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(2400, 1300)

        Start-Process $Exe | Out-Null
        $h = Get-MainWindow
        [W]::ShowWindow($h, 9) | Out-Null
        [W]::MoveWindow($h, 300, 80, $Width, $Height, $true) | Out-Null
        [W]::SetForegroundWindow($h) | Out-Null
        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(2400, 1300)
        Start-Sleep -Seconds 12   # let thoughts and images load

        [W]::SendMessage($h, 0x0086, [IntPtr]1, [IntPtr]::Zero) | Out-Null
        [W]::SendMessage($h, 0x0006, [IntPtr]1, [IntPtr]::Zero) | Out-Null
        Start-Sleep -Milliseconds 200

        $r = New-Object W+RECT
        [W]::GetWindowRect($h, [ref]$r) | Out-Null
        $eb = New-Object W+RECT
        [W]::DwmGetWindowAttribute($h, 9, [ref]$eb, [System.Runtime.InteropServices.Marshal]::SizeOf($eb)) | Out-Null

        $bmp = New-Object System.Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $hdc = $g.GetHdc()
        [W]::PrintWindow($h, $hdc, 2) | Out-Null   # PW_RENDERFULLCONTENT (needed for WebView2)
        $g.ReleaseHdc($hdc); $g.Dispose()

        $cropRect = New-Object System.Drawing.Rectangle ($eb.L - $r.L), ($eb.T - $r.T), ($eb.R - $eb.L), ($eb.B - $eb.T)
        $cropped = $bmp.Clone($cropRect, $bmp.PixelFormat)
        $bmp.Dispose()

        $file = Join-Path $Out "win-$Lang-$theme.png"
        $cropped.Save($file, [System.Drawing.Imaging.ImageFormat]::Png)
        $cropped.Dispose()
        Write-Host "captured $file"
    }
} finally {
    if ($null -ne $origLight) {
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value $origLight
    }
}
