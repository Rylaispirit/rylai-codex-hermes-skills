<#
.SYNOPSIS
    Install the Rylai skill bundle for Claude.

.DESCRIPTION
    Copies every folder in skills\ into the Claude skill directory.
    The default target is $HOME\.claude\skills, which is available in every
    Claude session. Use -Project to install into .\.claude\skills for the
    current project only, or -Target to pick an explicit directory.

.EXAMPLE
    .\install-claude.ps1
    .\install-claude.ps1 -Force
    .\install-claude.ps1 -Project
    .\install-claude.ps1 -Target D:\shared\claude-skills
#>
param(
    [switch]$Force,
    [switch]$Project,
    [string]$Target
)

$ErrorActionPreference = "Stop"
$SourceRoot = Join-Path $PSScriptRoot "skills"

if ($Target) {
    $TargetRoot = $Target
} elseif ($Project) {
    $TargetRoot = Join-Path (Get-Location) ".claude\skills"
} else {
    $TargetRoot = Join-Path $HOME ".claude\skills"
}

$TargetParent = Split-Path -Parent ([System.IO.Path]::GetFullPath($TargetRoot))
$BackupRoot = Join-Path $TargetParent "rylai-skill-backups"
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Installed = 0
$Skipped = 0

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null

Get-ChildItem -LiteralPath $SourceRoot -Directory | ForEach-Object {
    $SkillTarget = Join-Path $TargetRoot $_.Name
    if (Test-Path -LiteralPath $SkillTarget) {
        if (-not $Force) {
            Write-Warning "Skip existing skill: $($_.Name). Re-run with -Force to replace."
            $script:Skipped++
            return
        }
        $Backup = Join-Path (Join-Path $BackupRoot $Stamp) $_.Name
        New-Item -ItemType Directory -Force -Path (Split-Path $Backup -Parent) | Out-Null
        Copy-Item -LiteralPath $SkillTarget -Destination $Backup -Recurse
        Remove-Item -LiteralPath $SkillTarget -Recurse -Force
    }
    Copy-Item -LiteralPath $_.FullName -Destination $SkillTarget -Recurse
    Write-Host "Installed $($_.Name)"
    $script:Installed++
}

Write-Host ""
Write-Host "Installed $Installed skill(s), skipped $Skipped."
Write-Host "Target: $TargetRoot"
if ($Force) {
    Write-Host "Backup root: $BackupRoot"
}
Write-Host "Start a new Claude session so the skills are picked up."
