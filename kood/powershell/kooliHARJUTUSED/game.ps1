<#
Äraarvamise mäng. Numbrid 1-100
Tagauks
Kui mäng on läbi, siis küsitakse nime ja koos käikudega/sammudega salvestatakse see faili
#>
$pc_nr = Get-Random -Minimum 1 -Maximum 100
[System.Boolean]$game_over = $false
$Global:steps = 0   #Globaalne muutuja sammud
$filename = Join-Path -Path $PSScriptRoot -ChildPath "result.txt"
Clear-Host
Write-Host $pc_nr $filename #Kontrolliks
Clear-Host


function writeToFile {
    $name = Read-Host "Mängija nimi"
    ($name, $Global:steps -join ",") | Out-File -FilePath $filename -Append #Append lisab failinime alati juurde
    
}
#writeToFile