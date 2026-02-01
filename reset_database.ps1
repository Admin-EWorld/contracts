# Database Reset Script for Contract Generator
# Run this script when you need to reset the database after schema changes

Write-Host "🔄 Resetting Contract Generator Database..." -ForegroundColor Cyan
Write-Host ""

# Check if database exists
if (Test-Path "contracts.db") {
    Write-Host "📁 Found existing database file" -ForegroundColor Yellow
    
    # Try to delete the database
    try {
        Remove-Item "contracts.db" -Force -ErrorAction Stop
        Write-Host "✅ Database deleted successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Cannot delete database - it's locked by a running process" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please follow these steps:" -ForegroundColor Yellow
        Write-Host "1. Stop the uvicorn server (Press CTRL+C in the server terminal)" -ForegroundColor White
        Write-Host "2. Run this script again" -ForegroundColor White
        Write-Host ""
        exit 1
    }
} else {
    Write-Host "ℹ️  No existing database found" -ForegroundColor Blue
}

Write-Host ""
Write-Host "✅ Database reset complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Start the server: uvicorn main:app --host 0.0.0.0 --port 4000" -ForegroundColor White
Write-Host "2. The database will be created automatically with the new schema" -ForegroundColor White
Write-Host ""
