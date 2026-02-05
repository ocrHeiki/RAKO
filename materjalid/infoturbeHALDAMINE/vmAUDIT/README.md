```
###############################################################################
#                                                                             #
#   █████   █████           ████                                              #
#  ▒▒███   ▒▒███           ▒▒███                                              #
#   ▒███    ▒███   ██████   ▒███  █████ █████ █████ ████ ████████             #
#   ▒███    ▒███  ▒▒▒▒▒███  ▒███ ▒▒███ ▒▒███ ▒▒███ ▒███ ▒▒███▒▒███            #
#   ▒▒███   ███    ███████  ▒███  ▒███  ▒███  ▒███ ▒███  ▒███ ▒▒▒             #
#    ▒▒▒█████▒    ███▒▒███  ▒███  ▒▒███ ███   ▒███ ▒███  ▒███                 #
#      ▒▒███     ▒▒████████ █████  ▒▒█████    ▒▒████████ █████                #
#       ▒▒▒       ▒▒▒▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒      ▒▒▒▒▒▒▒▒ ▒▒▒▒▒                 #
#                                                                             #
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüsi raamistik           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      ocrHeiki  -  (https://github.com/ocrHeiki)           |   #
#   |   STATUS:      Aktiivne uurimine                                    |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
```

# Projekti ülevaade

## Miks "VALVUR"?
Nimi **VALVUR** valiti tähistama kompromissitut järelevalvet ja analüütilist täpsust. Infosüsteemi uurimisel ei piisa vaid pealiskaudsest vaatlusest – vaja on "valvurit", kes märkab ka kõige väiksemaid kõrvalekaldeid tavapärasest käitumisest, kaardistab sündmuste kronoloogia ja tuvastab ründaja poolt jäetud varjatud jäljed.

ASCII-põhine visuaalne identiteet on kummardus klassikalisele küberkaitse ja *forensics* kultuurile, kus selgus ja funktsionaalsus on alati esikohal.

## Ülesande kirjeldus
Kasutaja Pille Porgand märkas 16.11.2025 tööpäeva jooksul (umbes kell 16:11), et arvutiga toimub midagi ebatavalist. Töö tegemise ajal logiti ta ootamatult süsteemist välja. Pärast uuesti sisse logimist ilmusid ekraanile korraks tundmatud aknad, mida varem polnud esinenud. 

Uurimise eesmärk on kaardistada ründe kronoloogia, tuvastada ründaja sisenemispunkt, võimalikud loodud püsivusmehhanismid (kontod, skriptid, teenused) ning hinnata andmete kompromiteerimise ulatust.

## Ligipääsu andmed uurijale
Intsidendi lahendamiseks ja süsteemide analüüsiks on loodud eraldi IR (Incident Response) konto:
* **Kasutaja:** `IR`
* **Parool:** `Parool123456@`

## Analüüsitavad süsteemid
* **TRL-DC01**: Windows Server 2019 (Domeenikontroller)
* **TRL-INFRA01**: Windows Server 2016 (Rakendusserver)
* **TRL-WIN10-01**: Windows 10 Pro (Kasutaja tööjaam)

## Uurimisprotsessi struktuur
Uurimine on jaotatud kaheks peamiseks etapiks:
1. [**01. etapp: Logifailide analüüs**](01.etapp.md) - Süsteemsete sündmuselogide (`.evtx`) analüüs.
2. [**02. etapp: Tööjaama süvaanalüüs**](02.etapp.md) - Isoleeritud keskkonnas (VM) läbiviidav audit kasutades **VALVUR** tööriistakomplekti.

## Tulemused ja raport
Kõik analüüsi käigus kogutud faktid, tuvastatud ründeindikaatorid (IOC) ja lõppjäreldused dokumenteeritakse faili:
* 👉 [**leiud.md**](leiud.md)
