# Publish the site to GitHub Pages.
# Run from this folder:  .\deploy.ps1  [-Message "what changed"]
#
# NOTE: index.html is now maintained by hand (it diverged from the artifact
# fragment — see build.py). Edit index.html directly; this script just commits
# and pushes it. build.py is kept only as a preview generator.
param([string]$Message = "Update landing page")

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

git add -A
git commit -m $Message
if ($?) { git push }

Write-Output "Live at https://smart-mortgage-insurance.github.io/ (allow a minute for the build)"
