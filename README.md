Basic Web Vulnerability Scanner (Lab-Only)

Small Python utility to probe a deliberately vulnerable target (e.g., OWASP Juice Shop / DVWA) for reflected XSS and basic SQLi indicators.
The scanner is non-destructive and meant for lab use only.

Legal & Ethics : 
This tool is for local labs and training. Do not scan systems you don’t own or lack explicit permission to test.

Why I built it : 

I wanted a hands-on security project that shows: crawling/request logic, safe probing, basic detection heuristics, and clean reporting – all on a confined target.

What it does (current scope) : 

Sends safe probes to search endpoints/forms.

Flags potential reflected XSS when a unique token is echoed back unescaped.

Flags potential SQL injection using non-destructive variations and common DB error fingerprints.

Prints a short summary and can output JSON (planned).

It’s not a full DAST tool. The goal is a clear, minimal PoC that’s easy to read, extend, and reason about.

Lab setup (tested with) : 

OWASP Juice Shop running locally on http://127.0.0.1:3000/
(Docker: docker run --rm -p 3000:3000 bkimminich/juice-shop)

Python 3.10+

Quick start :
# create & activate a venv (optional)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
# or just: pip install requests


Run the basic test:

python sqli_test.py --url http://127.0.0.1:3000/rest/products/search


Run the advanced test:

python sqli_advanced_test.py --url http://127.0.0.1:3000/rest/products/search --mode all --timeout 5

Example output : 
=== Normal Search ===
GET /search?q=apple -> 200 (text/html; charset=utf-8)

=== SQLi Tests ===
[+] "' OR '1'='1" -> suspicious length delta (+912) | no WAF block | no redirect
[ ] "' Or 'a'='a"  -> no clear signal
[ ] "--" variant   -> blocked (403)

=== XSS Tests ===
[+] token echoed unescaped at /rest/products/search?q=XSS_TOKEN_93f1...
    evidence: appears in HTML body without &lt; &gt; escaping

Project structure :
/scanner
  sqli_test.py              # minimal test (baseline vs. one sqli/xss probe)
  sqli_advanced_test.py     # multiple probes, simple heuristics & summary
  requirements.txt
  README.md

Heuristics used :

SQLi

Compare response length vs. baseline (weak signal, used as hint only).

Search for common DB error snippets (e.g., "SQL syntax", "near '", "SQLiteException", "SequelizeDatabaseError").

Status codes, redirects, or unusual content types.

Reflected XSS :

Inject a unique token (e.g., XSS_TOKEN_<random>) instead of <script>.

Flag if the token appears unescaped in the HTML/JSON (no &lt;/&gt;) or inside attributes.

Design choices :

Keep it small and readable over “clever”.

Prefer non-destructive probes.

Treat findings as “possible”/“suspicious” with explicit evidence, not absolute truths.

Roadmap :

 CLI with argparse (--url, --mode, --json-report)

 Robust exception handling, timeouts, and retries

 Basic crawler for same-origin links + form enumeration

 JSON/HTML report with counts, timings, and evidence

 Stored-XSS check (delayed verification)

 Rate limiting and concurrency via asyncio

Limitations :

Heuristics only; may yield false positives/negatives.

Currently targets a single endpoint; crawler/forms are planned.

No authentication flows yet.

Safety notes :

Disabled any destructive payloads by design.

Throttle requests in future versions; even labs can be overwhelmed.

License :

MIT

Photos : 

<img width="641" height="252" alt="Screenshot 2025-09-18 181627" src="https://github.com/user-attachments/assets/3fdf0739-8914-49bf-ae38-198a2da05e4f" />

<img width="637" height="410" alt="תצלום מסך 1" src="https://github.com/user-attachments/assets/e97c478d-43ae-4989-bca0-fe4b0a7d2c48" />
<img width="526" height="147" alt="תצלום מסך 2" src="https://github.com/user-attachments/assets/6b6dccf1-83fe-400c-b1c7-a2ce95399989" />

