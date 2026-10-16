import re
import sys
from bs4 import BeautifulSoup
import urllib.request
import struct

sys.stdout.reconfigure(encoding='utf-8')

text = open(r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\136\content.md', encoding='utf-8', errors='ignore').read()
soup = BeautifulSoup(text, 'html.parser')

figs = soup.select('.ui-pdp-gallery__figure, .ui-pdp-gallery__picture, [data-zoom]')
for i, f in enumerate(figs[:4]):
    img = f.select_one('img')
    if img:
        print(f"Fig {i}:", {k: v for k, v in img.attrs.items() if 'src' in k or 'zoom' in k})

all_ml = list(set(re.findall(r'https://http2\.mlstatic\.com/D_[^\s"\'<>]+', text)))
print(f"\nTotal mlstatic occurrences: {len(all_ml)}")
# filter for images of product
prod_imgs = [u for u in all_ml if '752412-MLB117311996485' in u]
print("Variations of product image 752412-MLB117311996485:")
for u in prod_imgs:
    print(" ", u)

def get_jpeg_size(data):
    i = 0
    if data[0:2] != b'\xff\xd8':
        return None
    i += 2
    while i < len(data):
        marker, = struct.unpack('>H', data[i:i+2])
        i += 2
        if marker in (0xffc0, 0xffc2):
            length, bits, height, width = struct.unpack('>H B H H', data[i:i+7])
            return width, height
        else:
            length, = struct.unpack('>H', data[i:i+2])
            i += length
    return None

headers = {'User-Agent': 'Mozilla/5.0'}
base_id = '752412-MLB117311996485_092026'

candidates = [
    f'https://http2.mlstatic.com/D_NQ_NP_{base_id}-O.jpg',
    f'https://http2.mlstatic.com/D_NQ_NP_2X_{base_id}-F.jpg',
    f'https://http2.mlstatic.com/D_NQ_NP_2X_{base_id}-O.jpg',
    f'https://http2.mlstatic.com/D_NQ_NP_4X_{base_id}-F.jpg',
    f'https://http2.mlstatic.com/D_NQ_NP_{base_id}-F.jpg',
    f'https://http2.mlstatic.com/D_NQ_NP_2X_{base_id}-F.webp',
    f'https://http2.mlstatic.com/D_NQ_NP_{base_id}-O.webp',
]

print("\nTesting candidate URLs resolution:")
for c in candidates:
    try:
        req = urllib.request.Request(c, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            sz = get_jpeg_size(data)
            print(f"  {len(data)//1024} KB | {sz} | {c}")
    except Exception as e:
        print(f"  FAILED ({e}) | {c}")
