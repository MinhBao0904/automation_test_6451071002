[CmdletBinding()]
param(
    [ValidateSet("chrome", "edge")]
    [string]$Browser = "chrome",
    [int]$Pause = 5,
    [string]$Case,
    [switch]$Headless
)

$ErrorActionPreference = "Stop"
$pytestArgs = @("-m", "pytest", "--browser=$Browser", "--pause=$Pause")
if ($Case) { $pytestArgs += "--case=$Case" }
if ($Headless) { $pytestArgs += "--headless" }

& python @pytestArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

npx --yes --package=allure-commandline allure generate allure-results --clean -o allure-report
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Allure report created: $((Resolve-Path 'allure-report/index.html').Path)"
