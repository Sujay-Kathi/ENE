Write-Host "Starting FutureLens services..." -ForegroundColor Cyan

# Start Backend
Write-Host "Starting FastAPI Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --reload --port 8000"

# Wait a few seconds to let backend initialize
Write-Host "Waiting for backend to initialize..." -ForegroundColor DarkGray
Start-Sleep -Seconds 5

# Start Frontend
Write-Host "Starting React Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Both services have been started in separate windows!" -ForegroundColor Green
Write-Host "Backend API: http://127.0.0.1:8000"
Write-Host "Frontend Dashboard: http://localhost:5173"
