import urllib.request
import re
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Let's check html of houzez
req = urllib.request.Request('https://houzez-1.netlify.app/', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        imgs = re.findall(r'https://images\.unsplash\.com/[^\s"\'<>]+', html)
        print('Found unsplash in html:', len(imgs))
except Exception as e:
    print('Error:', e)
