import urllib.request
import re
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

req = urllib.request.Request('https://houzez-1.netlify.app/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    imgs = re.findall(r'https://images\.unsplash\.com/[^\s"\'<>]+', html)

# Clean url
villa_url = imgs[0]
if '?' in villa_url:
    base = villa_url.split('?')[0]
    villa_url = base + '?auto=format&fit=crop&w=1200&q=85'

print('Downloading villa image from:', villa_url)
dest_raw = r'C:\Users\mahen\OneDrive\Desktop\CodeYari\code_yari\media\portfolio\houzez_raw.jpg'
dest_cover = r'C:\Users\mahen\OneDrive\Desktop\CodeYari\code_yari\media\portfolio\houzez_cover.jpg'

req2 = urllib.request.Request(villa_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req2) as resp:
    with open(dest_raw, 'wb') as f:
        f.write(resp.read())

raw = Image.open(dest_raw).convert('RGB')
w, h = raw.size
target_w, target_h = 800, 480
scale = max(target_w / w, target_h / h)
resized = raw.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
rw, rh = resized.size
crop_x = (rw - target_w) // 2
crop_y = (rh - target_h) // 2
cropped = resized.crop((crop_x, crop_y, crop_x + target_w, crop_y + target_h))

# Subtle luxury dark gradient overlay
overlay = Image.new('RGBA', (target_w, target_h), (10, 15, 30, 0))
draw = ImageDraw.Draw(overlay)

for y in range(target_h):
    alpha = int(90 + 150 * (y / target_h))
    draw.line([(0, y), (target_w, y)], fill=(15, 23, 42, alpha))

final = Image.alpha_composite(cropped.convert('RGBA'), overlay)
draw_f = ImageDraw.Draw(final)

# Gold / Blue Luxury Pill Badge
draw_f.rounded_rectangle([30, 30, 240, 64], radius=16, fill=(37, 99, 235, 220))
draw_f.text((45, 38), "REAL ESTATE PLATFORM", fill=(255, 255, 255, 255))

# Bottom title text
draw_f.text((32, 380), "HOUZEZ", fill=(255, 255, 255, 255))
draw_f.text((32, 415), "Luxury Real Estate & Property Marketplace", fill=(226, 232, 240, 240))

final = final.convert('RGB')
final.save(dest_cover, quality=95)
print('Saved houzez_cover.jpg successfully')
