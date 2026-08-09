param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$SourceRoot = Join-Path $PSScriptRoot "skills"
$TargetRoot = Join-Path $HOME ".agents\skills"
$BackupRoot = Join-Path $TargetRoot ".rylai_backups"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

Get-ChildItem -LiteralPath $SourceRoot -Directory | ForEach-Object {
    $Target = Join-Path $TargetRoot $_.Name
    if (Test-Path -LiteralPath $Target) {
        if (-not $Force) {
            Write-Warning "Skip existing skill: $($_.Name). Re-run with -Force to replace."
            return
        }
        $Backup = Join-Path (Join-Path $BackupRoot $Stamp) $_.Name
        New-Item -ItemType Directory -Force -Path (Split-Path $Backup -Parent) | Out-Null
        Copy-Item -LiteralPath $Target -Destination $Backup -Recurse
        Remove-Item -LiteralPath $Target -Recurse -Force
    }
    Copy-Item -LiteralPath $_.FullName -Destination $Target -Recurse
    Write-Host "Installed $($_.Name)"
}
