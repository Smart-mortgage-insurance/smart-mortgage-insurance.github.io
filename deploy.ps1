# Rebuild index.html from the artifact fragment and publish it to GitHub Pages.
# Run from this folder:  .\deploy.ps1  [-Message "what changed"]
param([string]$Message = "Update landing page")

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

& "C:/Users/אסתי/AppData/Local/Programs/Python/Python312/python.exe" build.py

git add -A
git commit -m $Message
if ($?) { git push }

Write-Output "Live at https://smart-mortgage-insurance.github.io/ (allow a minute for the build)"
