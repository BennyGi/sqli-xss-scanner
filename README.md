# Basic Web Vulnerability Scanner (Lab-Only)

Small Python utility that probes a deliberately vulnerable target (**OWASP Juice Shop / DVWA**) for **basic SQL injection indicators** and **reflected XSS**.  
The scanner is **non-destructive** and intended for **local lab use only**.

> **Legal & Ethics** — Use strictly on lab targets you own or have explicit permission to test.  
> Do **not** scan external systems.

---

Screenshots (from local run):
<img width="641" height="252" alt="Screenshot 2025-09-18 181627" src="https://github.com/user-attachments/assets/2c9c47e0-e875-4de1-881a-7259ab601971" />
<img width="637" height="410" alt="תצלום מסך 1" src="https://github.com/user-attachments/assets/ce44a367-df41-4521-8a03-05b02684fced" />
<img width="526" height="147" alt="תצלום מסך 2" src="https://github.com/user-attachments/assets/181ac065-26d4-4b3d-bb1b-05eb7cb8e584" />


---

##  Why this project?:
I wanted a compact **hands-on security project** that demonstrates:
- HTTP request logic
- Safe probing
- Simple heuristics
- Clean reporting

Without pretending to be a full DAST scanner.

---

## What it does (current scope):
- Sends safe probes to a **search endpoint/form**.
- Flags potential **SQLi** using:
  - Non-destructive variations  
  - Common DB error fingerprints
- Flags potential **reflected XSS** when a unique token is echoed back **unescaped**.
- Prints a **short human-readable summary** (JSON/HTML report planned).

---

## Lab Setup (tested with):
- **Target**: OWASP Juice Shop running locally at `http://127.0.0.1:3000/`
- **Quick start with Docker**:
  docker run --rm -p 3000:3000 bkimminich/juice-shop
Requirements: 
Python 3.10+
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt   # or simply: pip install requests

Project Layout:
/scanner
  ├── sqli_test.py              # minimal baseline vs. one SQLi/XSS probe
  ├── sqli_advanced_test.py     # multiple probes + heuristics & summary
  ├── requirements.txt
  ├── README.md
  └── /docs                     # screenshots (see examples above)
Usage:
url = "http://127.0.0.1:3000/rest/products/search"
Run:
python sqli_test.py
python sqli_advanced_test.py
Example Output (abridged):

=== Normal Search ===
200 OK ... (first 200 chars)

=== SQLi Tests ===
[+] "' OR '1'='1"  ⇒ Vulnerable (length delta +xxx / error fingerprint matched)
[ ] "' Or 'a'='a'" ⇒ Not Vulnerable
[ ] "--" variant   ⇒ Blocked (403)

=== XSS Test ===
[+] token XSS_TOKEN_93f1... ⇒ Reflected (possible XSS).


Heuristics:
SQLi:
Compare response length vs. baseline (weak hint, used cautiously)
Look for DB error snippets (e.g., SQL syntax, near ', SQLite, SequelizeDatabaseError)
Note unusual status codes, redirects, or content type

Reflected XSS:
Inject unique token like XSS_TOKEN_<random> instead of <script>
Flag if it appears unescaped in HTML/JSON (no &lt; &gt;) or inside attributes

Design Choices:
Keep scripts small and readable
Prefer non-destructive probes
Label findings as “possible / suspicious” with explicit evidence, not absolute truths

Results (sample, local):
Target: single endpoint (/rest/products/search)
Requests: ~5–10
Findings: 1 SQLi hint + 1 reflected XSS hint
Runtime: < 2s on a laptop

Roadmap:
CLI via argparse (--url, --mode, --timeout, --json-report)
Robust exception handling & retries
Simple crawler + form enumeration
JSON/HTML report with counts & evidence
Stored-XSS check (delayed verification)
Throttling + optional asyncio

Known Limitations:
Heuristics may cause false positives/negatives
Current focus: single endpoint only
No authentication flows yet

Safety Notes:
Destructive payloads are intentionally excluded
Even in labs: add throttling to avoid overwhelming services

License:
MIT


Author:
Benny Giorno 
