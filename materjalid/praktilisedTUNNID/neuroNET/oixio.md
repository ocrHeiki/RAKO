## Wireshark

### Filtrid
Microsoft:
```
!(ip.geoip.as_org == "MICROSOFT-CORP-MSN-AS-BLOCK")
```
Kerberose filter:
```
!(nbns) && !(llmnr) && !(kerberos) && !(svcctl) && !(msrpc)
```
Mõlemad koos:
```
!(ip.geoip.as_org == "MICROSOFT-CORP-MSN-AS-BLOCK") && !(nbns) && !(llmnr) && !(kerberos)
```
