# ITSK25_Heiki_generator.ps1
# Loob juhuslike numbritega maatriksi ja salvestab faili 'output.txt'
# Autor: ocrHeiki

do {
    $suurus = Read-Host "Sisesta maatriksi suurus (3–10)"
} while ([int]$suurus -lt 3 -or [int]$suurus -gt 10)

$maatriks = @()
for ($i = 0; $i -lt $suurus; $i++) {
    $rida = @()
    for ($j = 0; $j -lt $suurus; $j++) {
        $arv = Get-Random -Minimum 1 -Maximum 100
        $rida += ("{0:D2}" -f $arv)
    }
    $maatriks += ,$rida
}

$outFile = "output.txt"
$maatriks | ForEach-Object { ($_ -join " ") } | Set-Content $outFile

Write-Host "Maatriks suurusega ${suurus}x${suurus} salvestatud faili 'output.txt'."
Write-Host "`nFaili sisu:"
Get-Content $outFile
