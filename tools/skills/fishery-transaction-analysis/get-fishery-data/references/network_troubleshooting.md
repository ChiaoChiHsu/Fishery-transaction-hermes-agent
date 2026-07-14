# Network/DNS Troubleshooting for MOA API

When accessing the Taiwan Ministry of Agriculture Open Data API (`data.moa.gov.tw`) you may encounter errors such as:
```
curl: (6) Could not resolve host: data.moa.gov.tw
```
This indicates a DNS resolution failure, not a problem with the API itself.

## Common causes
1. **No internet connection** – Verify you can reach other sites (e.g., `curl https://www.google.com`).
2. **Firewall or corporate proxy** – Some environments block external DNS or require a proxy. Set `http_proxy`/`https_proxy` environment variables accordingly.
3. **Local DNS cache issue** – Try flushing the DNS cache (`sudo dscacheutil -flushcache` on macOS) or using a different DNS server (e.g., 8.8.8.8).
4. **System DNS misconfiguration** – Ensure `/etc/resolv.conf` contains valid nameserver entries.

## Diagnostic steps
```bash
# 1. Test basic connectivity
curl -I https://www.google.com

# 2. Try to resolve the host
nslookup data.moa.gov.tw

# 3. Ping the host (ICMP may be blocked, but still useful)
ping -c 3 data.moa.gov.tw
```
If the above commands fail, address the network issue before re‑running the fishery data script.

## Work‑around for temporary issues
- Use a VPN or different network.
- Download the data on another machine and transfer the JSON file.

These steps should resolve most DNS‑related failures when fetching fishery transaction data.
