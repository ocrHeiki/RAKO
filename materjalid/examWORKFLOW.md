# 🚀 EKSAMI TÖÖVOOG & SPRIKKER — TEAM 10 (Kaughalduse võimekusega)

See töövoog on optimeeritud nii, et esmalt jäädvustatakse puhta võrgu seisund ning seejärel rakendatakse automatiseeritud ja käsitsi forensikat, kahjustamata olemasolevaid ründetõendeid. Kõik uuritavate masinate tulemused saadetakse automaatselt üle SCP tagasi Kali töölauale.

---

## 📅 ETTEVALMISTUSKORD (Tee kohe laboris hommiku alguses / kloonimise ajal)

Kuna kooliserveri ligipääs oli piiratud, käivita need käsud oma Kali terminalis **kohe laboris esimese asjana** (sel ajal kui masinad vSphere'is kloonivad). See võtab aega vaid hetke:

```bash
# 1. Uuenda pakette ja paigalda põhitööriistad + FreeRDP (Windowsi kaughalduseks)
sudo apt update
sudo apt install -y mc nmap zenmap-kbx net-tools iproute2 freerdp2-x11

# 2. Käivita Kali enda SSH server (Vajalik, et VALVUR master saaks raportid Kalisse saata)
sudo systemctl enable ssh
sudo systemctl start ssh

# 3. Vaata ja kirjuta üles oma Kali täpne labori-IP (Seda on vaja VALVUR-i seadistamiseks)
ip a | grep "inet "
