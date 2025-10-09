function New-TestFile {
    <#
    .SYNOPSIS
        Loob testifaile määratud arvul juhusliku sisu ja laiendiga.
    .DESCRIPTION
        Funktsioon loob faile failihalduse harjutamiseks...
    .PARAMETER Count
        Mitu faili luua (kohustuslik)
    .PARAMETER Names
        Failinimed mida kasutada. Üks kuni mitu. Vaikimis $env:USERNAME
    .PARAMETER Path
        Kuhu failid luuakse. Vaikimisi Desktop\katsetus
    .PARAMETER ExtensionFile
        Faililaiendite loetelu. Vaikimisi extensions.txt mooduli kaustas.
    .EXAMPLE
        New-TestFile -Count 5
        Loob 5 faili kasutades sisseloginud kasutajanime failinimeks
    .EXAMPLE
        New-TestFile -Count 3 -Names "Aruanne", "Mari", "Jüri"
        Loob 3 juhusliku faili etteantud nimedega    
    #>

    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)] #kohustuslik parameeter
        [ValidateRange(1,1000)] 
        [int]$Count,

        [Parameter(Mandatory = $false)]
        [string[]]$Names,

        [Parameter(Mandatory = $false)]
        [string]$Path = "$env:USERPROFILE\Desktop\katsetus",

        [Parameter(Mandatory = $false)]
        [string]$ExtensionFile = "$PSScriptRoot\extension.txt" #peale viimast ei panda koma
    )

    # Kui nimed puuduvad, kasuta kasutajanime
    if (-not $Names -or $Names.Count -eq 0) {
        $Names = @($env:USERNAME)
        Write-Verbose "Kasutan vaikimisi nime $env:USERNAME"
    }
    
    # Kas laiendite fail on olemas
    if (-not (Test-Path -Path $ExtensionFile)) {
        Write-Error "Laiendite faili ei leitud: $ExtensionFile"
        Write-Host "Loo laiendite fail ja lisa laiendid"
        return
    }   
    
    # Loe laiendid faili
    $Extensions = Get-Content $ExtensionFile | Where-Object { 
        $_.Trim() -ne ""} | ForEach-Object { $_.Trim() }
   
        if ($Extensions.Count -eq 0) {
        Write-Error "Laiendite faili on tühi: $ExtensionFile"
        return
    }

    Write-Verbose "Leitud $($Extensions.Count) laiendit."
    
    # Loo kaust kui puudub
    if (-not (Test-Path -Path $Path)) {
        New-Item -Path $Path -ItemType Directory -Force | Out-Null
        Write-Host "Loodud kaust: $Path"
    }
    # Loome failist loenduri
    $createdCount = 0
    $skippedCount = 0
    $createdFiles = @()

    # Genereeri failid
    for ($i = 0; $i -lt $Count; $i++) {
    
    # Vali juhuslik nimi
    $randomName = $Names | Get-Random

    # Vali juhuslik laiend
    $randomExtension = $Extensions | Get-Random       
           
    #Koosta failinimi
    $fileName = "$randomName.$randomExtension"
    $fullPath = Join-Path $Path $fileName

    # Kas fail on juba olemas
    if (Test-Path -Path $fullPath) {
        Write-Warning "Fail juba olemas, vahelejätmine: $fileName"
        $skippedCount++
        continue
    
    }
    
    # Kas selline kombinatsioon on juba loodud
    if ($createdFiles -contains $fileName) {
        Write-Warning "Selle nimega fail on juba olemas, jätan vahele."
        $skippedCount++
        continue
    }

    # Genereeri juhuslik sisu
    $contentSize = Get-Random -Minimum 100 -Maximum 1025
    $randomContent = -join ((1..$contentSize) | ForEach-Object { 
        [char](Get-Random -Minimum 32 -Maximum 127) 
    })

    # Loo fail
    try {
        Set-Content -Path $fullPath -Value $randomContent -Encoding UTF8 -ErrorAction Stop
        $createdCount++
        $createdFiles += $fileName
        Write-Verbose "Loodud $fileName ($contentSize baiti)"
    } catch {
        Write-Error "Viga faili loomisel ($fileName): $_"
        $skippedCount++
    }
    # Teata tulemustest
    Write-Host "Loodud faile: $createdCount"
    if($skippedCount -gt 0) {
        Write-Host "Vahele jäetud (duplikaadid): $skippedCount"
    }    

    Write-Host "Asukoht: $Path"

    # Tagasta objekt tulemusega
    [PSCustomObject]@{
        CreatedCount = $createdCount
        SkippedCount = $skippedCount
        Location = $Path
        Files = $createdFiles
    }
    }
}