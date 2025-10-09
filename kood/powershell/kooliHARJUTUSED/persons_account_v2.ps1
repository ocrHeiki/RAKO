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
$dst = Join-Path -Path $PSScriptRoot -ChildPath ".\Persons_account_v2.csv"
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

$content = [System.IO.File]::ReadAllLines($src, [System.Text.Encoding]::UTF8)


# Loeme originaalfaili ja töötleme ridasid
$content | Select-Object -Skip 1 | ForEach-Object {
  $parts = $_.Split(";") # Tükeldame rea semikoolonist
  $date_str = $parts[2] # Kolmas element on sünniaeg
  $isValid = [DateTime]::ParseExact($date_str, $pattern, $null)
  if($isValid){
      $date = [DateTime]::ParseExact($date_str, $pattern, $null)
      if($date.Year -ge 1990 -and $date.Year -le 1999) {
          $counter++
            
          $first_name = $parts[0] #Eesnimi
          $last_name = $parts[1]  #Perenimi

            #Eemaldame tühiku ja sidekriipsu eesnimest
          $first_name = $first_name -replace " ", ""
          $first_name = $first_name -replace "-", ""

            #Loome kasutajanime
          $username = Remove-Diacritics($first_name, $last_name -join ".").ToLower()

            #Loome eposti
          $email = $username + $domain

            #Teeme massiiivi veergudest
          $array = $parts[0], $parts[1], $parts[2], $username, $email

            #Teeme uue rea faili
          $new_line = $array -join ";"

            #Write-Host $new_line
          Out-File $dst -Append -InputObject $new_line
        }
   }
   
}
Write-Host "Valmis, $counter tk."
