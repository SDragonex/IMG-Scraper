import os
import sys
import re
import json
import csv
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\d.chaker\Documents\IMG-Scraper"
STEPS_DIR = r"C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps"
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
INBRIMA_DIR = os.path.join(DOWNLOADS_DIR, "matchbox_inbrima")
ROLY_DIR = os.path.join(DOWNLOADS_DIR, "matchbox_roly_toys")

ROLY_STEPS = [
    227, 228, 229, 231, 232, 233, 234, 235,
    136, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 225, 226
]

INBRIMA_STEPS = [
    195, 241, 242, 243, 244, 245, 247, 248, 249, 250, 251,
    294, 295, 296, 297, 298, 300, 301, 302, 303, 304,
    306, 307, 308, 309, 310, 312, 313, 314, 315,
    451, 452, 453, 454, 455, 457, 458, 459, 460, 461,
    463, 464, 465, 466, 467,
    511, 512, 513, 514, 515, 517, 518, 519, 520, 521,
    538, 540, 542, 544, 548, 550, 552, 556, 558, 560,
    562, 564, 566,
    607, 609, 611, 613, 615, 617, 619
]

with open(os.path.join(DOWNLOADS_DIR, "models_catalog.json"), "r", encoding="utf-8") as f:
    cat = json.load(f)

def sanitize_folder_name(name, max_len=50):
    clean = re.sub(r'[\\/*?:"<>|]', '', name)
    clean = re.sub(r'\s+', '_', clean.strip())
    return clean[:max_len]

def extract_gallery_images(step_num):
    fpath = os.path.join(STEPS_DIR, str(step_num), "content.md")
    if not os.path.exists(fpath):
        return []
    html_text = open(fpath, encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html_text, "html.parser")
    
    figs = soup.select('.ui-pdp-gallery__figure, .ui-pdp-gallery__picture, [data-zoom]')
    img_ids = []
    seen = set()
    
    for f in figs:
        img = f.select_one('img')
        if not img:
            continue
        src = img.get('data-zoom') or img.get('src') or img.get('data-src') or ''
        m = re.search(r'(?:D_Q_NP_|D_NQ_NP_)(?:2X_)?([0-9A-Za-z_-]+)-[A-Z]', src)
        if m:
            base_id = m.group(1)
            if base_id not in seen:
                seen.add(base_id)
                img_ids.append(base_id)
                
    if not img_ids:
        all_matches = re.findall(r'(?:D_Q_NP_|D_NQ_NP_)(?:2X_)?([0-9A-Za-z_-]+)-[A-Z]', html_text)
        for base_id in all_matches:
            if base_id not in seen:
                seen.add(base_id)
                img_ids.append(base_id)
                
    return img_ids

def match_step_to_item(step_num, items):
    fpath = os.path.join(STEPS_DIR, str(step_num), "content.md")
    if not os.path.exists(fpath):
        return None
    html_text = open(fpath, encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html_text, "html.parser")
    can = soup.find('link', rel='canonical')
    if can and can.get('href'):
        can_url = can['href'].split('#')[0].strip()
        can_up = can_url.split('/')[-1]
        for it in items:
            clean_link = it['link'].split('#')[0].strip()
            if clean_link == can_url or clean_link.split('/')[-1] == can_up:
                return it
                
    for it in items:
        clean_link = it['link'].split('#')[0].strip()
        up = clean_link.split('/')[-1]
        if up and up in html_text:
            return it
            
    # Fallback to ID
    for it in items:
        if it['id'] in html_text:
            return it
            
    return None

def download_one_photo(img_id, target_file):
    # Check if we already have the FULL 1200px HD version (> 85 KB)
    if os.path.exists(target_file) and os.path.getsize(target_file) > 85000:
        return True
        
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # Priority 1: Full 1200px zoom HD image
    candidates = [
        f'https://http2.mlstatic.com/D_NQ_NP_2X_{img_id}-F.jpg',
        f'https://http2.mlstatic.com/D_NQ_NP_{img_id}-F.jpg',
        f'https://http2.mlstatic.com/D_NQ_NP_2X_{img_id}-O.jpg',
        f'https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.jpg',
        f'https://http2.mlstatic.com/D_NQ_NP_2X_{img_id}-F.webp',
        f'https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp',
    ]
    
    best_data = None
    for cand in candidates:
        try:
            req = urllib.request.Request(cand, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                # If we got a full HD image (> 60KB), save and return immediately!
                if len(data) > 60000:
                    with open(target_file, 'wb') as f_out:
                        f_out.write(data)
                    return True
                elif len(data) > 1000 and best_data is None:
                    best_data = data
        except Exception:
            continue
            
    if best_data:
        with open(target_file, 'wb') as f_out:
            f_out.write(best_data)
        return True
        
    return False

# Collect tasks
download_tasks = []

print("=== Processing Roly Toys steps ===")
for s in ROLY_STEPS:
    it = match_step_to_item(s, cat['roly_toys'])
    if not it:
        print(f"Warning: Step {s} could not be matched to a Roly Toys item")
        continue
    img_ids = extract_gallery_images(s)
    folder_slug = f"{it['id']}_{sanitize_folder_name(it['title'])}"
    item_folder = os.path.join(ROLY_DIR, folder_slug)
    os.makedirs(item_folder, exist_ok=True)
    
    photo_paths = []
    for idx, img_id in enumerate(img_ids, 1):
        filename = f"photo_{idx:02d}.jpg"
        target_file = os.path.join(item_folder, filename)
        rel_path = f"matchbox_roly_toys/{folder_slug}/{filename}"
        photo_paths.append(rel_path)
        download_tasks.append((img_id, target_file))
        
    it['photos'] = photo_paths
    it['photos_count'] = len(photo_paths)
    print(f"Roly [{it['id']}]: {len(photo_paths)} photos planned -> {folder_slug[:45]}")

print("\n=== Processing Inbrima steps ===")
for s in INBRIMA_STEPS:
    it = match_step_to_item(s, cat['inbrima'])
    if not it:
        print(f"Warning: Step {s} could not be matched to an Inbrima item")
        continue
    img_ids = extract_gallery_images(s)
    folder_slug = f"{it['id']}_{sanitize_folder_name(it['title'])}"
    item_folder = os.path.join(INBRIMA_DIR, folder_slug)
    os.makedirs(item_folder, exist_ok=True)
    
    photo_paths = []
    for idx, img_id in enumerate(img_ids, 1):
        filename = f"photo_{idx:02d}.jpg"
        target_file = os.path.join(item_folder, filename)
        rel_path = f"matchbox_inbrima/{folder_slug}/{filename}"
        photo_paths.append(rel_path)
        download_tasks.append((img_id, target_file))
        
    it['photos'] = photo_paths
    it['photos_count'] = len(photo_paths)
    print(f"Inbrima [{it['id']}]: {len(photo_paths)} photos planned -> {folder_slug[:45]}")

# Ensure any item without multi-photo still has its single photo listed
for it in cat['roly_toys']:
    if 'photos' not in it or not it['photos']:
        loc = it.get('local_file', '')
        rel = f"matchbox_roly_toys/{os.path.basename(loc)}" if loc else ""
        it['photos'] = [rel] if rel else []
        it['photos_count'] = len(it['photos'])

for it in cat['inbrima']:
    if 'photos' not in it or not it['photos']:
        loc = it.get('local_file', '')
        rel = f"matchbox_inbrima/{os.path.basename(loc)}" if loc else ""
        it['photos'] = [rel] if rel else []
        it['photos_count'] = len(it['photos'])

print(f"\nTotal image download tasks queued: {len(download_tasks)}")

# Run downloads with ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=16) as executor:
    futures = {executor.submit(download_one_photo, img_id, target_file): (img_id, target_file) for img_id, target_file in download_tasks}
    done = 0
    success = 0
    for fut in as_completed(futures):
        res = fut.result()
        done += 1
        if res:
            success += 1
        if done % 40 == 0 or done == len(download_tasks):
            print(f"Downloaded {done}/{len(download_tasks)} photos (Success: {success})")

# Save updated JSON catalog
catalog_path = os.path.join(DOWNLOADS_DIR, "models_catalog.json")
with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)

# Save updated CSV catalog
csv_path = os.path.join(DOWNLOADS_DIR, "models_catalog.csv")
with open(csv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['category', 'id', 'title', 'photos_count', 'photos', 'link'])
    writer.writeheader()
    for it in cat['inbrima']:
        writer.writerow({
            'category': 'Matchbox Inbrima',
            'id': it.get('id', ''),
            'title': it.get('title', ''),
            'photos_count': it.get('photos_count', 0),
            'photos': ';'.join(it.get('photos', [])),
            'link': it.get('link', '')
        })
    for it in cat['roly_toys']:
        writer.writerow({
            'category': 'Matchbox Roly Toys',
            'id': it.get('id', ''),
            'title': it.get('title', ''),
            'photos_count': it.get('photos_count', 0),
            'photos': ';'.join(it.get('photos', [])),
            'link': it.get('link', '')
        })

print("\nSuccessfully updated models_catalog.json and models_catalog.csv with FULL HD galleries!")
