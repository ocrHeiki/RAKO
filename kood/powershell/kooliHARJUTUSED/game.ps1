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

function Show-Scoreboard {
    $content = Get-Content -Path $filename
    foreach ($line in $content) {
        Write-Host $line.split(";")
    }
}

function LetsPlay {
    [int]$user_nr = Read-Host "Sisesta number"
    $Global:steps++ #Global:steps += 1
    $game_over = $false

    if(($user_nr -gt $pc_nr) -and ($user_nr -ne 1000)) {
      Write-Host "Väiksem"

    } elseif (($user_nr -lt $pc_nr) -and ($user_nr -ne 1000)) {
    } elseif (($user_nr -eq $pc_nr) -and ($user_nr -ne 1000)) {
        Write-Host "Leidsid õige numbri $Global:steps sammuga."
        $game_over = $true
    } elseif (($user_nr -eq 1000)) {
        Write-Host "Leidsid mu nõrga koha. Õige number on $pc_nr"
    }   
        return $game_over #Tagastab tulemuse $true või $false
}
while($game_over -eq $false) {
    $game_over =  LetsPlay
    if($game_over){
        writeToFile
        Show-Scoreboard
        $answer = Read-Host "Kas mängime veel? (J/E)"
        if($answer -eq "J") {
            $pc_nr = Get-Random -Minimum 1 -Maximum 100
            [System.Boolean]$game_over = $false
            $Global:steps = 0
           
}
}
}
Write-Host "Mäng läbi"