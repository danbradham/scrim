$env:SCRIM_SHELL="powershell.exe"
$env:SCRIM_PATH="scrim_out.ps1"
$env:SCRIM_AUTO_WRITE="{{auto_write}}"
$env:SCRIM_SCRIPT = $MyInvocation.MyCommand.Definition

# Call the real python cli
python -m {{entry_point}} $args

if (Test-Path $env:SCRIM_PATH) {
    Try{
        & ".\$env:SCRIM_PATH"
    }
    Catch {
        $content = Get-Content $env:SCRIM_PATH | Out-String
        Write-Host 'Failed to execute scrim...'
        Write-Host ''
        Write-Host $content
    }
    Remove-Item $env:SCRIM_PATH
}

# Remove variables
Remove-Item Env:SCRIM_SHELL
Remove-Item Env:SCRIM_PATH
Remove-Item Env:SCRIM_AUTO_WRITE
Remove-Item Env:SCRIM_SCRIPT
