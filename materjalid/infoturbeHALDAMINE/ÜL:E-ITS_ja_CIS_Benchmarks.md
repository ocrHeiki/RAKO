# E-ITS ja CIS Benchmarks
**Autor:** Triin Muulmann
---

- 100 punkti
- Ülesanne: Infovarade turvameetmete hindamine ja
rakendamine (E-ITS + CIS Benchmarks)

---
## Eesmärk:

Õppida analüüsima ja hindama oma virtuaalkeskkonnas olevate
infovarade (operatsioonisüsteemid ja teenused) infoturbe taset vastavalt:

E-ITS
(Eesti infoturbestandardi) nõuetele
CIS
Benchmarks soovitustele


b) Mis on CIS Benchmarks?


CIS Benchmarks on rahvusvahelised juhendid
turvameetmete seadistamiseks konkreetsetele süsteemidele (nt Windows Server,
Ubuntu, MySQL jne).

Need annavad samm-sammult soovitused, kuidas süsteem turvaliselt seadistada (nt
"keela anonüümne ligipääs", "lülita välja mittevajalikud
teenused", "aktiveeri tulemüür").


---
Praktiline osa

---
## Ülesanne 1: E-ITS põhine infovarade turvakontroll


###Sammud:

### Valige
3 virtuaalmasinat (nt Windows Server, Ubuntu Server, pfSense,
Debian jms).
### Valige
3 teenust (nt DHCP, DNS, failiserver, veebiserver, SQL server,
Active Directory).
### Koostage
tabel, kus on kirjas:
- infovara
- nimi
- rakendatavad
- turvameetmed (E-ITS põhjal)
kas
- meede on rakendatud (✅ / ❌
- / ei kohaldu)
kuidas
kontrollisite meedet
kuidas
seadistate vastavat meedet

---
🧾 Näidistabel – E-ITS
turvameetmete kontroll


![E-ITS](eITS.png)

---
## Ülesanne 2: CIS Benchmarks põhine süsteemi kontroll

### Sammud:


Vali
üks infovara (nt Ubuntu Server).
Ava CIS Benchmarks leht ja
vali sobiv juhend (nt CIS Ubuntu Linux 22.04 LTS Benchmark). Saad
siit vaadata https://github.com/jonathanbglass/cis-benchmarks
Vali
10 sinu arvates kõige olulisemat turvameedet.
Koosta
ja täida järgmine tabel.



🧾 Näidistabel – CIS
Benchmark meetmete kontroll

![CIS](cis_benchmark.png)





Infovara




CIS meede




Rakendatud (X)




Kuidas kontrollite?




Kuidas seadistate?







Ubuntu Server




1.1.1.1 – Keela cramfs kernelimoodul




✅




Kontrollin `lsmod




grep cramfs`






Ubuntu Server




1.1.2 – Keela USB massmälu tugi




❌




Kontrollin `lsmod




grep usb_storage`






Ubuntu Server




2.2.1.2 – SSH root login keelatud




✅




Kontrollin sshd_config failist




PermitRootLogin no






Ubuntu Server




3.2.2 – Aegunud paroolid keelatud




✅




Kontrollin chage -l kasutaja




Seadistan PASS_MAX_DAYS 90 failis /etc/login.defs






Ubuntu Server




3.3.1 – Failide õigused /etc/passwd




✅




Kontrollin ls -l /etc/passwd




chmod 644 /etc/passwd






Ubuntu Server




3.6.1 – Tulemüür on aktiveeritud




✅




Käsk sudo ufw status




sudo ufw enable






Ubuntu Server




4.1.1 – Auditd teenus töötab




❌




Kontrollin systemctl status auditd




sudo apt install auditd ja systemctl enable auditd






Ubuntu Server




4.2.1 – Logfailid on kaitstud




✅




Kontrollin ls -l /var/log/




chmod 600 /var/log/auth.log






Ubuntu Server




5.1.1 – Keela anonüümne FTP




✅




Kontrollin vsftpd.conf failist




anonymous_enable=NO






Ubuntu Server




6.2.1 – Kontrolli mittekasutatavad kontod




❌




sudo passwd -S kasutaja




Deaktiveeri usermod -L kasutaja











---
📋 Kokkuvõte / esitamise
nõuded:


Esitada tuleb:


Täidetud
E-ITS meetmete tabel (3 OS + 3 teenust)
Täidetud
CIS Benchmark tabel (1 infovara, 10 meedet)
Lühike
kokkuvõte (0,5–1 lk), kus kirjeldad:
milliseid
probleeme avastasid kontrollimisel;
milliseid
meetmeid rakendasid või parandasid;
millised
on kõige olulisemad turvameetmed sinu süsteemis ja miks.
