# Directly specify the root directory to search for Python installations
$searchDirectory = "C:\Users\User\AppData\Local\Programs\Python"

# Search for Python installations within this directory
$pythonPath = Get-ChildItem -Path $searchDirectory -Recurse -Filter python.exe -ErrorAction SilentlyContinue | Select-Object -First 1

# Check if a Python installation was found
if ($pythonPath) {
    # Use the first Python installation found in the search directory
    $pythonPath = $pythonPath.FullName
    Write-Host "Using Python from: $pythonPath"
} else {
    Write-Host "Python not found in $searchDirectory. Please install Python."
    exit
}

# Save the Python path for future use
$pythonPathFile = ".\python_path.txt"
if (Test-Path $pythonPathFile) {
    $savedPythonPath = Get-Content $pythonPathFile
    Write-Host "Using saved Python path: $savedPythonPath"
} else {
    Write-Host "Saving Python path: $pythonPath"
    Set-Content -Path $pythonPathFile -Value $pythonPath
}

# Ensure pip is available
$pipPath = "$($pythonPath)\Scripts\pip.exe"
if (-Not (Test-Path $pipPath)) {
    Write-Host "pip not found. Installing pip..."
    & $pythonPath -m ensurepip --upgrade
    $pipPath = "$($pythonPath)\Scripts\pip.exe"
}

# Check if the virtual environment exists, create it if it doesn't
if (-not (Test-Path ".\.venv")) {
    Write-Host "Creating virtual environment..."
    & $pythonPath -m venv .venv
}

# Activate the virtual environment
$activateScript = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..."
    & $activateScript
} else {
    Write-Host "Activation script not found. Please ensure the virtual environment is correctly set up."
    exit
}

# Install dependencies from requirements.txt if it exists
if (Test-Path "requirements.txt") {
    Write-Host "requirements.txt found. Installing dependencies..."
    
    # Ensure pip is available in the virtual environment, using the virtual environment's pip path
    $pipPath = ".\.venv\Scripts\pip.exe"
    if (-Not (Test-Path $pipPath)) {
        Write-Host "pip not found in virtual environment. Installing pip..."
        & $pythonPath -m ensurepip --upgrade
    }

    # Install the modules
    & $pipPath install --upgrade -r requirements.txt
} else {
    Write-Host "requirements.txt not found."
}

Write-Host "Modules installation complete."
