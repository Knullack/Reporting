# getModules.ps1

# Check if Python is installed
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Host "Python is not installed. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if the virtual environment exists
$venvPath = ".\.venv"
if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$activateScript = ".\.venv\Scripts\Activate.ps1"
& $activateScript

# Check if requirements.txt exists, and create it if it doesn't
if (-not (Test-Path "requirements.txt")) {
    Write-Host "requirements.txt not found. Creating it..." -ForegroundColor Yellow
    pip freeze > requirements.txt
    Write-Host "requirements.txt has been created with current modules." -ForegroundColor Green
} else {
    Write-Host "requirements.txt found." -ForegroundColor Green
}

# Install dependencies from requirements.txt
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install --upgrade -r requirements.txt

Write-Host "Modules installation complete." -ForegroundColor Green
