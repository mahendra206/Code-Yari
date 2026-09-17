import urllib.request
import os
from PIL import Image, ImageDraw

# Download the actual poster from theteachmantra.com
poster_url = 'https://www.theteachmantra.com/media/popup_banners/poster-1_wuqhv6.jpg'
dest_raw = r'C:\Users\mahen\OneDrive\Desktop\CodeYari\code_yari\media\portfolio\teachmantra_poster_raw.jpg'
dest_cover = r'C:\Users\mahen\OneDrive\Desktop\CodeYari\code_yari\media\portfolio\teachmantra_cover.jpg'

req = urllib.request.Request(poster_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        with open(dest_raw, 'wb') as f:
            f.write(resp.read())
    print('Downloaded poster, size:', os.path.getsize(dest_raw))
except Exception as e:
    print('Download failed, using uploaded image:', e)
    # Fallback to the user-uploaded image
    dest_raw = r'C:\Users\mahen\.gemini\antigravity-ide\brain\686f7edd-8079-4c9d-9908-4b9622e18db9\.user_uploaded\media_1789547155211.png'

raw = Image.open(dest_raw).convert('RGB')
w, h = raw.size
print('Raw size:', w, h)

# Crop & resize to 800x480 cover
target_w, target_h = 800, 480
scale = max(target_w / w, target_h / h)
resized = raw.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
rw, rh = resized.size
crop_x = (rw - target_w) // 2
crop_y = (rh - target_h) // 2
cropped = resized.crop((crop_x, crop_y, crop_x + target_w, crop_y + target_h))

cropped.save(dest_cover, quality=95)
print('Saved teachmantra_cover.jpg (poster version) successfully')
