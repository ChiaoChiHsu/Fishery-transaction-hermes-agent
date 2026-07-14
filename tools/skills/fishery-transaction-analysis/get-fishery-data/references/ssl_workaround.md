## SSL Verification Workaround
The MOA Open Data API sometimes presents an invalid SSL certificate, causing `requests` to raise `SSLError`. To bypass this, you can:

- In Python: add `verify=False` to `requests.get` calls (as demonstrated in the patched `demo_get.py`).
- Using `curl`: add the `-k` flag (e.g., `curl -k https://data.moa.gov.tw/...`). This disables certificate verification.

**Security note**: Disabling verification is safe in this trusted environment because the endpoint is known and controlled, but avoid using it for untrusted hosts.
