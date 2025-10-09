<#
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned #Ainult allkirjastatud skriptid
Käivita see käsureal Administratorina

nii saab ka mitmerealist kommentaari lisada
#>
Clear-Host #Puhasta ekraan: cls
Get-Date #Näita tänast kuupäeva

$username = Read-Host -Prompt "Sisesta enda kasutajanimi"

if($username -eq $env:USERNAME) {
    Write-Host "Õige kasutajanimi"
} else {
    Write-Host "Vale kasutajanimi $username, eeldati: $env:USERNAME"
}

[int]$year = Read-Host "Sisesta aasta"
if($year -eq (Get-Date).Year){
    Write-Host "Käesolev aasta"
    } else {
    Write-Host "Mõni teine aasta: $year"
}

# Massiiv
$nums = @() #tühi massiiv
$nums += 5
$nums += 2
$nums += 6
$nums += Get-Random -Minimum 1 -Maximum 10

Write-Host $nums
Write-Host $nums[-1]
Write-Host $nums[$nums.Length - 1]

$num = 0 #Algväärtus
$num += 5 #num = num + 5
$num += 3
$num += Get-Random -Minimum 1 -Maximum 10

Write-Host $num
<#
Liida kokku kaks juhuslikku numbrit. Mõlemad on vahemikus 1-10.
Vastus on muutujas $random
#>
$random = (Get-Random -Minimum 1 -Maximum 10) + (Get-Random -Minimum 1 -Maximum 10)
Write-Host "Summa on $random"