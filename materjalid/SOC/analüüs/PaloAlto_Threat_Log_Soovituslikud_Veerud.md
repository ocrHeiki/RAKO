# Palo Alto Threat Log – Soovituslikud CSV veerud

See dokument määratleb, millised logiväljad on **SOC L1 analüütiku töövoos kõige olulisemad** ja millised võib jätta välja, et CSV fail oleks väiksem ja selgem.

---

## ✅ Olulised veerud (hoia alles)

- **Generate Time** – logisündmuse aeg  
- **Type** – logi tüüp (`THREAT`, `TRAFFIC`, jne)  
- **Threat ID/Name** – ohu nimi või signatuuri identifikaator  
- **From Zone / To Zone** – võrgutsoonide kontekst  
- **Source Address** – lähte IP-aadress  
- **Source User** – kasutaja (kui olemas)  
- **Severity** – kriitilisuse aste (Critical, High, Medium, Low)  
- **Destination Address** – siht IP-aadress  
- **To Port** – sihtport (nt 80, 443, 3389)  
- **Application** – rakendus või protokoll (http, ssl, ssh jne)  
- **Action** – kas `Allowed` või `Blocked`  
- **File Name / URL** – kui tegemist on failiohu või URL-iga  
- **Device Name / Device SN** – logi allika seade  
- **Rule** – turvapoliitika reegel, mis vastet andis  

---

## ➕ Täiendavad kasulikud (võid hoida, kui täidetud)

- **Source Country / Destination Country** – geograafiline asukoht  
- **NAT Source IP / NAT Dest IP** – NAT-iga seotud aadressid  
- **Session ID** – seansi unikaalne identifikaator  
- **Threat Category** – ohu kategooria (nt Malware, Reconnaissance)  

---

## ❌ Võib välja jätta (enamasti tühjad või L2/L3 analüütiku jaoks)

- **Dynamic User Group**, **Device OS Family**, **Device MAC**, **Container ID**  
- **Cloud Report ID**, **Cluster Name**, **Proxy Transaction**, **Tunnel ID**  
- **Monitor Tag**, **App SaaS**, **App Subcategory**, **App Technology**  
- **X-Forwarded-For IP** (vajalik ainult proxy logidega)  

---

## 🎯 L1 analüüsi põhiküsimused

1. Mis tüüp oht tuli? (Threat Name / Category)  
2. Kui tõsine see on? (Severity)  
3. Kas see lubati või blokeeriti? (Action)  
4. Kust see tuli? (Source Address / User / Country)  
5. Kuhu see läks? (Destination Address / Port / Application / Zone)  
6. Mis reegel selle vallandas? (Rule)  
7. Millal see juhtus? (Generate Time)  

Kõik ülejäänud väljad on kasulikud pigem **sügavamaks analüüsiks (L2/L3)** või järeluuringuteks.

---

📌 Nõuanne: kui CSV eksporti seadistad, alusta ainult soovitatud väljadega. Hiljem, kui vajad rohkem konteksti, lisa järk-järgult uusi välju.
