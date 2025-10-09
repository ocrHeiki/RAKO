<#
Luua etteantud kasutajate kasutajanimi ja epostiaadress
KASUTAJANIMI:
eesnimi.perenimi
eesnimes eeldada tõhi ja/või sidekriips Mari Liis, Mari-Liis
eemalda rõhumärgid ja täpitähed (ä,ö,ü,õ,š,ž)
kasutajanimi väikeste tähtedega
EPOSTIAADRESS:
kasutajanimi@asutus.com
KELLELE TEHA:
Sündinud 1990-1999 k.a.
UUE FAILI SISU ON:
Eesnnimi, Perenimi, Isikukood, Kasutajanimi, Epost
Eesnimi;Perenimi;Sünniaeg;Sugu;Isikukood <-- ORIGINAAL

https://stackoverflow.com/questions/7836670
#>


$src = Join-Path -Path $PSScriptRoot -ChildPath ".\Persons.csv"
$dst = Join-Path -Path $PSScriptRoot -ChildPath ".\Persons_account_v1.csv"
$domain = "@asutus.com"
$header = "Eesnimi;Perenimi;Sünniaeg;Sugu;Isikukood;Kasutajanimi;Epost"
$pattern = "dd.MM.yyyy" #kuupäeva formaat failis
$counter = 0

function Remove-Diacritics {
param ([String]$src = [String]::Empty)
  $normalized = $src.Normalize( [Text.NormalizationForm]::FormD )
  $sb = new-object Text.StringBuilder
  $normalized.ToCharArray() | % { 
    if( [Globalization.CharUnicodeInfo]::GetUnicodeCategory($_) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
      [void]$sb.Append($_)
    }
  }
  $sb.ToString()
}
# Kas uus fail on olemas
if(Test-Path $dst) {
    Remove-Item $dst
}
# Kirjutame uude faili päise
Out-File -FilePath $dst -Append -InputObject $header

# Loeme originaalfaili ja töötleme ridasid
Import-Csv $src -Delimiter ";" | ForEach-Object {
   $date_str = $_.Sünniaeg
   $isValid = [DateTime]::ParseExact($date_str, $pattern, $null)
   if($isValid){
        $date = [DateTime]::ParseExact($date_str, $pattern, $null)
        if($date.Year -ge 1990 -and $date.Year -le 1999) {
            $counter++
            
            $first_name = $_.Eesnimi
            $last_name = $_.Perenimi

            #Eemaldame tühiku ja sidekriipsu eesnimest
            $first_name = $first_name -replace " ", ""
            $first_name = $first_name -replace "-", ""

            #Loome kasutajanime
            $username = Remove-Diacritics($first_name, $last_name -join ".").ToLower()

            Write-Host $username
        }
   }
   
   #Write-Host $_
}

