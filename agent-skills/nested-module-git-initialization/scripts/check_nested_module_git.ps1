[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $ProjectRoot,

    [switch] $Initialize,

    [switch] $Json
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "check_nested_module_git.py"

$pythonCommand = $null

foreach ($candidate in @("python", "python3")) {
    $command = Get-Command $candidate -ErrorAction SilentlyContinue | Select-Object -First 1

    if ($null -ne $command) {
        $pythonCommand = $command.Source
        break
    }
}

if ($null -eq $pythonCommand) {
    [Console]::Error.WriteLine("Python 3 is required to run check_nested_module_git.ps1.")
    exit 127
}

$scriptArgs = @($pythonScript, "--project-root", $ProjectRoot)

if ($Initialize) {
    $scriptArgs += "--initialize"
}

if ($Json) {
    $scriptArgs += "--json"
}

& $pythonCommand @scriptArgs
exit $LASTEXITCODE
