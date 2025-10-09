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

