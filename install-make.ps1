if ((Get-Command make -ErrorAction SilentlyContinue)) {
    Write-Output "Make is already installed. If your make does not work, uninstall it and run this script again"
    exit
}

# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Output "Chocolatey is not installed. Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
} else {
    Write-Output "Chocolatey is already installed."
}

# Refresh the environment to recognize choco without reopening the shell
$env:Path += ";$($env:ProgramData)\chocolatey\bin"

# Check if make is installed
if (-not (Get-Command make -ErrorAction SilentlyContinue)) {
    Write-Output "make is not installed. Installing make..."
    choco install make -y
} else {
    Write-Output "make is already installed."
}
