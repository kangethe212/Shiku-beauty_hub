# Shiku Beauty Hub - Push to GitHub
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   PUSHING SHIKU BEAUTY HUB TO GITHUB" -ForegroundColor Magenta
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Configure Git
Write-Host "Configuring Git..." -ForegroundColor Yellow
git config user.email "bennymaish01@gmail.com"
git config user.name "Shiku Beauty Hub"

# Add files
Write-Host "Adding files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Shiku Beauty Hub - Complete beauty e-commerce website with 60 products, Jazzmin admin, WhatsApp integration"

# Set main branch
Write-Host "Setting main branch..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "Note: You'll need to enter your GitHub credentials" -ForegroundColor Green
git push -u origin main

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   PUSH COMPLETE!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "View your code at:" -ForegroundColor Yellow
Write-Host "https://github.com/kangethe212/Shiku-beauty_hub" -ForegroundColor Cyan
Write-Host ""
pause

