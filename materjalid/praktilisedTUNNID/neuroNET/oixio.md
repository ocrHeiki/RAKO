## Wireshark

### Filtrid

Hüümärk `!` filtri ees keelab seda otsingut

Microsoft:
```
!(ip.geoip.dst_org == "MICROSOFT-CORP-MSN-AS-BLOCK")
```
Kerberose filter:
```
!(nbns) && !(llmnr) && !(kerberos) && !(svcctl) && !(msrpc)
```
Mõlemad koos:
```
!(ip.geoip.dst_org == "MICROSOFT-CORP-MSN-AS-BLOCK") && !(nbns) && !(llmnr) && !(kerberos)
```
