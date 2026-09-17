import urllib.request
import re

req = urllib.request.Request('https://www.theteachmantra.com/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        for match in re.finditer(r'(?:src|href|url)\s*[:=]\s*["\']([^"\']+\.(?:png|jpg|jpeg|webp))["\']', html, re.IGNORECASE):
            print('Found:', match.group(1))
        # also search for popup or modal in html
        popups = re.findall(r'<div[^>]+id=["\'][^"\']*(?:popup|modal|banner)[^"\']*["\'][^>]*>[\s\S]{1,600}', html, re.IGNORECASE)
        for p in popups:
            print('Popup snippet:', p[:300])
except Exception as e:
    print('Error:', e)
