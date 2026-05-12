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
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  00_MITRE_ATTCK_juhend_vol2.md                        |   #
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   MITRE ATT&CK ründeahela ja logide seostamine.        |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

# MITRE ATT&CK ründeahela analüüs

See juhend aitab kaardistada logidest leitud sündmused vastavalt **MITRE ATT&CK** raamistikule. Ründe mõistmine läbi taktika aitab tuvastada ründaja järgmisi võimalikke samme.

## 1. Ründeahela etapid ja Windowsi logid

| Taktika (Tactic) | Tehnika (Technique) | Event ID | Logi allikas |
| :--- | :--- | :--- | :--- |
| **Initial Access** | Brute Force (T1110) | **4625** | Security |
| | Valid Accounts (T1078) | **4624** | Security |
| **Execution** | PowerShell (T1059.001) | **4104** | PowerShell Op |
| | Command/Scripting (T1059) | **4688** | Security |
| **Persistence** | New Service (T1543.003) | **4697, 7045** | System |
| | Create Account (T1136) | **4720** | Security |
| | Scheduled Task (T1053) | **4698** | Security |
| **Privilege Escalation** | Special Privileges (T1068) | **4672** | Security |
| | Group Membership (T1098) | **4732** | Security |
| **Defense Evasion** | Clear Logs (T1070.001) | **1102, 104** | Security/System |
| | Process Injection (T1055) | **4688** | Security |
| **Credential Access** | OS Credential Dumping (T1003) | **4663** | Security (LSASS) |
| **Lateral Movement** | Remote Desktop (T1021.001) | **4624 (Type 10)**| Security |
| | SMB/PsExec (T1021.002) | **5140, 5145** | Security |

## 2. Kuidas seda infot analüüsis kasutada?

1.  **Tuvasta anomaalia:** Kui leiad sündmuse **4697** (uue teenuse lisamine), vaata MITRE tabelist - see on **Persistence**. 
2.  **Laienda otsingut:** Ründaja tahab nüüd tõenäoliselt liikuda edasi **Credential Access** (paroolide vargus) või **Lateral Movement** (teistesse masinatesse liikumine) suunas.
3.  **Kasuta VALVUR skripte:** Otsi märksõnu nagu `mimikatz` (Credential Access) või `psexec` (Lateral Movement) kasutades skripti **03_otsing_marksonade_jargi.py**.

## 3. Sisselogimise tüübid (Logon Types)

Sündmuse **4624** (Successful Logon) puhul on kriitiline vaadata **Logon Type** välja:
*   **Type 2:** Interaktiivne (klaviatuuri taga masinas).
*   **Type 3:** Võrgu kaudu (tavaline failijagamine või rünne üle võrgu).
*   **Type 7:** Unlock (masina lukust lahtitegemine).
*   **Type 10:** Remote Interactive (**RDP** - ründajate lemmik).

---
*Mõistes ründaja taktikat, oled alati sammu võrra ees!*
