# 🤖 Checklist — VPN & networking

- [ ] VpnService only when VPN is the core functionality; declared in Play Console → `../rules/permissions/foreground_service_and_vpn.md`
- [ ] Traffic encrypted to the VPN server; no ad manipulation or data collection without disclosure
- [ ] Data safety form reflects any data processing
- [ ] Foreground service type `systemExempted`/`specialUse` justified where used
