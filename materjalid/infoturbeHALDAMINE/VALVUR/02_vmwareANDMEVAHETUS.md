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
#   |   PROJEKT:     VALVUR - VMware Andmevahetus                         |   #
#   |   FAILI NIMI:  03_vmwareANDMEVAHETUS.md                             |   #
#   |   LOODUD:      27.03.2026                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Andmevahetus rünnatud masina ja Kali vahel.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
```
# Turvaline andmete eraldamine (Forensic Data Extraction)

Käesolev juhend käsitleb meetodeid, kuidas eraldada logifaile ja muid tõendeid kompromiteeritud Windowsi masinast VMware keskkonnas nii, et säiliks andmete terviklikkus ja välditaks uuritava süsteemi "saastamist".

---

## MEETOD A: Virtuaalse vaheketa kasutamine (Soovitatav)

See on kõige puhtam meetod, kuna see ei nõua rünnatud masinas võrguühenduste loomist ega uue tarkvara paigaldamist.

### 1. samm: Loo uus andmevahetuse ketas
1. Ava VMware ja vali **Kali Linux** virtuaalmasin.
2. Mine: **Edit virtual machine settings** -> **Add...** -> **Hard Disk**.
3. Vali tüübiks **SCSI** või **NVMe** ja **Create a new virtual disk**.
4. Määra mahuks **10-20 GB** ja salvesta see ühe failina (nt `toendid.vmdk`).
5. Käivita Kali.

### 2. samm: Ketta ettevalmistamine Kalis
Tuvasta ketas ja vorminda see failisüsteemi, mida Windows tunneb (nt NTFS).
```bash
lsblk                      # Leia uus seade, nt /dev/sdb
sudo fdisk /dev/sdb        # Loo uus partitsioon (n -> p -> default -> w)
sudo mkfs.ntfs -L TOENDID /dev/sdb1
```
1. Lülita Kali Linux välja.
3. samm: Ketta ühendamine Windowsiga ja andmete kopeerimine
1. Mine Windowsi masina seadetesse: Add... -> Hard Disk.
2. Vali Use an existing virtual disk ja vali eelnevalt loodud toendid.vmdk.
3. Käivita Windows. Ketas ilmub uue draivina (nt E:).
4. Kopeeri (Copy) logid:
```
C:\Windows\System32\winevt\Logs\* -> E:\LOGID\.
```
6. Lülita Windows välja ja eemalda (Remove) ketas seadetest (valikutest vali "Remove", mitte "Delete from disk").
4. samm: Analüüs Kalis
1. Ühenda ketas tagasi Kali külge.
2. Käivita Kali ja haagi ketas külge:
```
sudo mount /dev/sdb1 /mnt
cd /mnt/LOGID
```
MEETOD B: SMB-serveri kaudu (Kiire meetod)
Kasuta seda juhul, kui masinad on samas isoleeritud sisevõrgus (LAN Segment) ja sa ei soovi masinaid taaskäivitada.
1. samm: Pane Kalis püsti vastuvõttev server
# Loo kaust ja käivita Impacket SMB server
```
mkdir ~/VALVUR/LOGID
sudo impacket-smbserver VALVUR ~/VALVUR/LOGID -smb2support
```
2. samm: Saada andmed Windowsist
Ava Windowsis Command Prompt (Admin):
```
net use Z: \\<KALI_IP>\VALVUR
xcopy C:\Windows\System32\winevt\Logs\*.evtx Z:\ /S
net use Z: /delete
```
Kriitilised märkused
• Ära lõika (Cut) faile, vaid alati kopeeri (Copy).
• Ajalised märkmed: Pane kirja kellaaeg, mil ühendasid välise ketta, et eristada enda tegevust ründaja tegevusest logides.
• Võrk: Kui kasutad Meetodit B, veendu, et masinad on Host-only või LAN Segment režiimis, et vältida pahavara levikut pärisvõrku.
