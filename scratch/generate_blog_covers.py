import os
import django
from PIL import Image, ImageDraw, ImageFont

import sys
sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from django.conf import settings
from apps.blog.models import BlogPost

os.makedirs(os.path.join(settings.MEDIA_ROOT, 'blog'), exist_ok=True)

def create_gradient(width, height, start_color, end_color):
    base = Image.new('RGBA', (width, height), start_color)
    top = Image.new('RGBA', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            factor = (x / width * 0.6) + (y / height * 0.4)
            mask_data.append(int(255 * factor))
    mask.putdata(mask_data)
    return Image.composite(top, base, mask)

W, H = 800, 450

try:
    font_code = ImageFont.truetype('consola.ttf', 16)
    font_badge = ImageFont.truetype('arialbd.ttf', 14)
    font_title = ImageFont.truetype('arialbd.ttf', 32)
    font_sub = ImageFont.truetype('arial.ttf', 18)
except Exception:
    font_code = font_badge = font_title = font_sub = ImageFont.load_default()

# 1. Django Framework Cover
img1 = create_gradient(W, H, (15, 23, 42), (30, 58, 138))
d1 = ImageDraw.Draw(img1)
for r in range(160, 40, -20):
    alpha = int(35 * (1 - r / 160))
    d1.ellipse((500 - r, 200 - r, 500 + r, 200 + r), fill=(59, 130, 246, alpha))

card1_box = [380, 80, 720, 360]
d1.rounded_rectangle(card1_box, radius=16, fill=(15, 23, 42, 230), outline=(59, 130, 246, 180), width=2)
d1.ellipse((405, 102, 417, 114), fill=(239, 68, 68, 255))
d1.ellipse((425, 102, 437, 114), fill=(245, 158, 11, 255))
d1.ellipse((445, 102, 457, 114), fill=(16, 185, 129, 255))

code_lines = [
    ('from django.urls import path', (96, 165, 250)),
    ('from . import views', (147, 197, 253)),
    ('', (255, 255, 255)),
    ('class EnterprisePlatform(App):', (52, 211, 153)),
    ('    speed = "blazing_fast"', (251, 191, 36)),
    ('    security = "bulletproof"', (251, 191, 36)),
    ('    scalable = True', (167, 139, 250)),
    ('', (255, 255, 255)),
    ('    def deploy(self):', (52, 211, 153)),
    ('        return "Success! 🚀"', (244, 114, 182)),
]
y_off = 135
for line, col in code_lines:
    d1.text((410, y_off), line, fill=col, font=font_code)
    y_off += 21

d1.rounded_rectangle([60, 110, 220, 142], radius=16, fill=(37, 99, 235, 60), outline=(59, 130, 246, 200), width=1)
d1.text((78, 118), 'PYTHON & DJANGO', fill=(147, 197, 253), font=font_badge)
d1.text((60, 165), 'Full-Stack\nArchitecture', fill=(255, 255, 255), font=font_title)
d1.text((60, 255), 'High-security backend\nbuilt for enterprise scale.', fill=(148, 163, 184), font=font_sub)
path1 = os.path.join(settings.MEDIA_ROOT, 'blog', 'cover_django.jpg')
img1.convert('RGB').save(path1, quality=92)


# 2. SEO Guide Cover
img2 = create_gradient(W, H, (24, 24, 27), (194, 65, 12))
d2 = ImageDraw.Draw(img2)
for r in range(160, 40, -20):
    alpha = int(35 * (1 - r / 160))
    d2.ellipse((520 - r, 210 - r, 520 + r, 210 + r), fill=(249, 115, 22, alpha))

card2_box = [380, 80, 720, 360]
d2.rounded_rectangle(card2_box, radius=16, fill=(24, 24, 27, 235), outline=(249, 115, 22, 180), width=2)
d2.rounded_rectangle([405, 105, 695, 145], radius=20, fill=(39, 39, 42), outline=(249, 115, 22, 120), width=1)
d2.text((425, 118), '🔍  how to rank #1 on google', fill=(212, 212, 216), font=font_code)

bars = [(430, 60), (480, 80), (530, 110), (580, 145), (630, 185)]
for x, val in bars:
    y_top = 330 - val
    d2.rounded_rectangle([x, y_top, x + 35, 330], radius=6, fill=(249, 115, 22, 220), outline=(251, 146, 60, 255), width=1)

d2.rounded_rectangle([60, 110, 210, 142], radius=16, fill=(234, 88, 12, 60), outline=(249, 115, 22, 200), width=1)
d2.text((78, 118), 'SEO STRATEGY', fill=(253, 186, 116), font=font_badge)
d2.text((60, 165), 'Rank #1 on\nGoogle Search', fill=(255, 255, 255), font=font_title)
d2.text((60, 255), 'Drive organic traffic &\nskyrocket qualified leads.', fill=(161, 161, 170), font=font_sub)
path2 = os.path.join(settings.MEDIA_ROOT, 'blog', 'cover_seo.jpg')
img2.convert('RGB').save(path2, quality=92)


# 3. Professional Website 2025 Cover
img3 = create_gradient(W, H, (30, 27, 75), (124, 58, 237))
d3 = ImageDraw.Draw(img3)
for r in range(160, 40, -20):
    alpha = int(35 * (1 - r / 160))
    d3.ellipse((520 - r, 210 - r, 520 + r, 210 + r), fill=(168, 85, 247, alpha))

card3_box = [380, 80, 720, 360]
d3.rounded_rectangle(card3_box, radius=16, fill=(15, 23, 42, 235), outline=(139, 92, 246, 180), width=2)
d3.rounded_rectangle([400, 100, 700, 130], radius=8, fill=(30, 27, 75), outline=(168, 85, 247, 80), width=1)
d3.ellipse((412, 110, 422, 120), fill=(239, 68, 68))
d3.ellipse((428, 110, 438, 120), fill=(245, 158, 11))
d3.ellipse((444, 110, 454, 120), fill=(16, 185, 129))
d3.rounded_rectangle([465, 107, 685, 123], radius=4, fill=(49, 46, 129))
d3.text((475, 109), 'https://yourbusiness.com', fill=(196, 181, 253), font=font_code)

d3.rounded_rectangle([415, 150, 685, 195], radius=10, fill=(49, 46, 129, 180))
d3.text((430, 162), '⚡  Speed: 99/100 Core Web Vitals', fill=(255, 255, 255), font=font_code)
d3.rounded_rectangle([415, 210, 685, 255], radius=10, fill=(49, 46, 129, 180))
d3.text((430, 222), '📱  100% Mobile & Responsive', fill=(255, 255, 255), font=font_code)
d3.rounded_rectangle([415, 270, 685, 315], radius=10, fill=(49, 46, 129, 180))
d3.text((430, 282), '🔒  Modern SSL, Security & Speed', fill=(255, 255, 255), font=font_code)

d3.rounded_rectangle([60, 110, 235, 142], radius=16, fill=(124, 58, 237, 60), outline=(168, 85, 247, 200), width=1)
d3.text((78, 118), 'WEB ESSENTIALS 2025', fill=(216, 180, 254), font=font_badge)
d3.text((60, 165), '10 Reasons For A\nModern Website', fill=(255, 255, 255), font=font_title)
d3.text((60, 255), 'Grow credibility, conversions\nand business value.', fill=(196, 181, 253), font=font_sub)
path3 = os.path.join(settings.MEDIA_ROOT, 'blog', 'cover_website2025.jpg')
img3.convert('RGB').save(path3, quality=92)

# Update database
p1 = BlogPost.objects.filter(slug__icontains='django').first()
if p1:
    p1.featured_image = 'blog/cover_django.jpg'
    p1.save()
    print('Updated p1 cover:', p1.title)

p2 = BlogPost.objects.filter(slug__icontains='seo').first()
if p2:
    p2.featured_image = 'blog/cover_seo.jpg'
    p2.save()
    print('Updated p2 cover:', p2.title)

p3 = BlogPost.objects.filter(slug__icontains='2025').first()
if p3:
    p3.featured_image = 'blog/cover_website2025.jpg'
    p3.save()
    print('Updated p3 cover:', p3.title)

print('Success! All blog covers created and linked in database.')
