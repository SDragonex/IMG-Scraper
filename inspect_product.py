import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

with open(r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\136\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
print('Page Title:', soup.title.string if soup.title else '')

# Look for gallery container
gallery_figures = soup.select('.ui-pdp-gallery__figure, .ui-pdp-gallery__picture, [data-zoom]')
print('Gallery figures found:', len(gallery_figures))

# Let's inspect images in the gallery specifically
imgs = []
for fig in gallery_figures:
    img = fig.select_one('img')
    if img:
        src = img.get('data-zoom') or img.get('src') or img.get('data-src')
        if src:
            imgs.append(src)

print(f'Gallery specific images: {len(imgs)}')
for im in imgs:
    print('  Figure image:', im)

# Also check all mlstatic images
all_imgs = set(re.findall(r'https://http2\.mlstatic\.com/D_[^\s"\'<>]+\.(?:jpg|webp)', text))
print('Total unique mlstatic URLs in page:', len(all_imgs))
