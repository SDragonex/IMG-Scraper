import os
import re
import sys
import json
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\d.chaker\Documents\antigravity\zealous-hopper"
STEPS_DIR = r"C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps"
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
INBRIMA_DIR = os.path.join(DOWNLOADS_DIR, "matchbox_inbrima")
ROLY_DIR = os.path.join(DOWNLOADS_DIR, "matchbox_roly_toys")

# Steps for Roly Toys (all 21 items)
# In order of list_roly_urls.py (items 1 to 21)
ROLY_STEPS = [
    227, 228, 229, 231, 232, 233, 234, 235,
    136, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 225, 226
]

# Steps for Inbrima
INBRIMA_STEPS = [
    195, 241, 242, 243, 244, 245, 247, 248, 249, 250, 251,
    294, 295, 296, 297, 298, 300, 301, 302, 303, 304,
    306, 307, 308, 309, 310, 312, 313, 314, 315
]

def extract_gallery_from_step(step_num):
    fpath = os.path.join(STEPS_DIR, str(step_num), "content.md")
    if not os.path.exists(fpath):
        return None
    html_text = open(fpath, encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html_text, "html.parser")
    
    # Try finding item ID from HTML or canonical URL
    item_id = None
    m_id = re.search(r'(MLB\d{7,12})', html_text)
    if m_id:
        item_id = m_id.group(1)
        
    title = soup.title.string.strip() if soup.title else ""
    title = re.sub(r'\s*\|\s*Mercado\s*Livre.*$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s*\|\s*Parcelamento\s*sem\s*juros.*$', '', title, flags=re.IGNORECASE)
    
    # Extract figures
    figs = soup.select('.ui-pdp-gallery__figure, .ui-pdp-gallery__picture, [data-zoom]')
    img_urls = []
    seen_ids = set()
    
    for f in figs:
        img = f.select_one('img')
        if not img:
            continue
        src = img.get('data-zoom') or img.get('src') or img.get('data-src') or ''
        m = re.search(r'(?:D_Q_NP_|D_NQ_NP_)(?:2X_)?([0-9A-Za-z_-]+)-[A-Z]', src)
        if m:
            base_id = m.group(1)
            if base_id not in seen_ids:
                seen_ids.add(base_id)
                img_urls.append(base_id)
                
    # If no figures found, search all mlstatic in DOM
    if not img_urls:
        all_matches = re.findall(r'(?:D_Q_NP_|D_NQ_NP_)(?:2X_)?([0-9A-Za-z_-]+)-[A-Z]', html_text)
        for base_id in all_matches:
            if base_id not in seen_ids:
                seen_ids.add(base_id)
                img_urls.append(base_id)
                
    return {
        'step': step_num,
        'item_id': item_id,
        'title': title,
        'image_ids': img_urls
    }

print("Checking Roly Toys steps:")
roly_data = []
for s in ROLY_STEPS:
    d = extract_gallery_from_step(s)
    if d:
        roly_data.append(d)
        print(f"Step {s}: ID={d['item_id']}, Imgs={len(d['image_ids'])}, Title={d['title'][:40]}")

print("\nChecking Inbrima steps:")
inbrima_data = []
for s in INBRIMA_STEPS:
    d = extract_gallery_from_step(s)
    if d:
        inbrima_data.append(d)
        print(f"Step {s}: ID={d['item_id']}, Imgs={len(d['image_ids'])}, Title={d['title'][:40]}")

print(f"\nTotal Roly Toys listings with full gallery: {len(roly_data)}")
print(f"Total Inbrima listings with full gallery: {len(inbrima_data)}")
