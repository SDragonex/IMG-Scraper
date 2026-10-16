import os
import sys
import re
import json
import csv
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

# Ensure download directories exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')
INBRIMA_DIR = os.path.join(DOWNLOADS_DIR, 'matchbox_inbrima')
ROLY_DIR = os.path.join(DOWNLOADS_DIR, 'matchbox_roly_toys')

os.makedirs(INBRIMA_DIR, exist_ok=True)
os.makedirs(ROLY_DIR, exist_ok=True)

# Load catalog
with open(os.path.join(BASE_DIR, 'catalog.json'), 'r', encoding='utf-8') as f:
    raw_cat = json.load(f)

# Filtering Roly Toys
ROLY_EXCLUDE = [
    'roly poly', 'roly-poly', 'pet', 'gato', 'bebê', 'bebe',
    'tumbler', 'wobbler', 'chocalho', 'dinosaur', 'dino',
    'banho', 'pelúcia', 'pato', 'pinguim', 'sprays', 'puppy'
]

filtered_roly = []
for item in raw_cat.get('roly_toys', []):
    t_lower = item['title'].lower()
    if any(ex in t_lower for ex in ROLY_EXCLUDE):
        continue
    filtered_roly.append(item)

filtered_inbrima = raw_cat.get('inbrima', [])

print(f"Items to download:")
print(f" - Matchbox Inbrima: {len(filtered_inbrima)}")
print(f" - Matchbox Roly Toys: {len(filtered_roly)}")

def sanitize_filename(title, max_len=60):
    clean = re.sub(r'[\\/*?:"<>|]', '', title)
    clean = re.sub(r'\s+', '_', clean.strip())
    return clean[:max_len]

def download_image(item, target_dir):
    url = item.get('img_thumb', '')
    item_id = item.get('id', 'item')
    title = item.get('title', 'model')
    
    clean_title = sanitize_filename(title)
    filename = f"{item_id}_{clean_title}.jpg"
    target_path = os.path.join(target_dir, filename)
    
    # If already downloaded, skip
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        item['local_file'] = os.path.relpath(target_path, BASE_DIR)
        return True, item_id, target_path, "cached"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    candidates = []
    
    # Candidate 1: High-res JPG
    # Candidate 2: High-res WEBP
    # Candidate 3: Full original
    m = re.search(r'(?:D_Q_NP_|D_NQ_NP_)(?:2X_)?([0-9A-Za-z_-]+)-[A-Z]', url)
    if m:
        img_id = m.group(1)
        candidates.append(f'https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.jpg')
        candidates.append(f'https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp')
        candidates.append(f'https://http2.mlstatic.com/D_NQ_NP_2X_{img_id}-F.webp')
    if url:
        candidates.append(url)
        
    for cand in candidates:
        try:
            req = urllib.request.Request(cand, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                if len(data) > 1000:
                    with open(target_path, 'wb') as f_out:
                        f_out.write(data)
                    item['local_file'] = os.path.relpath(target_path, BASE_DIR)
                    return True, item_id, target_path, cand
        except Exception:
            continue
            
    return False, item_id, None, "failed"

# Download tasks
tasks = []
with ThreadPoolExecutor(max_workers=12) as executor:
    for item in filtered_inbrima:
        tasks.append(executor.submit(download_image, item, INBRIMA_DIR))
    for item in filtered_roly:
        tasks.append(executor.submit(download_image, item, ROLY_DIR))
        
    success_count = 0
    fail_count = 0
    for future in as_completed(tasks):
        success, item_id, path, src = future.result()
        if success:
            success_count += 1
        else:
            fail_count += 1
            print(f"Failed to download image for: {item_id}")
            
        if (success_count + fail_count) % 50 == 0:
            print(f"Progress: {success_count + fail_count}/{len(tasks)} (Success: {success_count}, Failed: {fail_count})")

print(f"\nDownloading complete! Success: {success_count}, Failed: {fail_count}")

# Save JSON metadata
with open(os.path.join(INBRIMA_DIR, 'catalog_inbrima.json'), 'w', encoding='utf-8') as f:
    json.dump(filtered_inbrima, f, ensure_ascii=False, indent=2)

with open(os.path.join(ROLY_DIR, 'catalog_roly_toys.json'), 'w', encoding='utf-8') as f:
    json.dump(filtered_roly, f, ensure_ascii=False, indent=2)

with open(os.path.join(DOWNLOADS_DIR, 'models_catalog.json'), 'w', encoding='utf-8') as f:
    json.dump({'inbrima': filtered_inbrima, 'roly_toys': filtered_roly}, f, ensure_ascii=False, indent=2)

# Save CSV metadata
csv_path = os.path.join(DOWNLOADS_DIR, 'models_catalog.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['category', 'id', 'title', 'price', 'local_file', 'link', 'img_high_res'])
    writer.writeheader()
    for item in filtered_inbrima:
        writer.writerow({
            'category': 'Matchbox Inbrima',
            'id': item.get('id', ''),
            'title': item.get('title', ''),
            'price': item.get('price', ''),
            'local_file': item.get('local_file', ''),
            'link': item.get('link', ''),
            'img_high_res': item.get('img_high_res', '')
        })
    for item in filtered_roly:
        writer.writerow({
            'category': 'Matchbox Roly Toys',
            'id': item.get('id', ''),
            'title': item.get('title', ''),
            'price': item.get('price', ''),
            'local_file': item.get('local_file', ''),
            'link': item.get('link', ''),
            'img_high_res': item.get('img_high_res', '')
        })

print(f"Saved CSV and JSON catalogs in {DOWNLOADS_DIR}")
