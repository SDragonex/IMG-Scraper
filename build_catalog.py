import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

inbrima_files = [
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\8\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\32\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\66\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\70\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\72\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\78\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\80\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\84\content.md',
]

roly_files = [
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\30\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\34\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\52\content.md',
    r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\88\content.md',
]

def extract_items(file_list, category):
    results = {}
    for fpath in file_list:
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        cards = soup.select('.poly-card')
        for card in cards:
            t_el = card.select_one('.poly-component__title, .ui-search-item__title')
            title = t_el.get_text(strip=True) if t_el else ''
            
            # Filter relevance
            t_lower = title.lower()
            if category == 'inbrima':
                if not ('inbrima' in t_lower or 'imbrima' in t_lower or 'manaus' in t_lower):
                    continue
            elif category == 'roly_toys':
                if not ('roly' in t_lower or 'roly toys' in t_lower or 'roly-toys' in t_lower):
                    continue
                
            link_el = card.select_one('a')
            link = link_el['href'] if link_el and 'href' in link_el.attrs else ''
            
            p_el = card.select_one('.poly-price__current, .price-tag-fraction')
            price = p_el.get_text(strip=True) if p_el else ''
            
            img_el = card.select_one('img')
            img_src = img_el.get('data-src') or img_el.get('src') if img_el else ''
            
            # Extract MLB ID
            mlb_m = re.search(r'(MLB-?\d+)', link)
            item_id = mlb_m.group(1).replace('-', '') if mlb_m else None
            if not item_id:
                # Try from img_src
                img_m = re.search(r'(MLB\d+)', img_src)
                if img_m:
                    item_id = img_m.group(1)
                else:
                    item_id = str(hash(title))
            
            # Derive high-res image URL
            # Example: https://http2.mlstatic.com/D_Q_NP_2X_680952-MLB119019252443_102026-E--inbrima-matchbox-miniatura-carrinho-1-mod-rod-b079.webp
            # -> https://http2.mlstatic.com/D_NQ_NP_680952-MLB119019252443_102026-O.jpg
            high_res_img = img_src
            m_img = re.search(r'(?:D_Q_NP_|D_NQ_NP_)(?:2X_)?([0-9A-Za-z_-]+)-[A-Z]', img_src)
            if m_img:
                clean_img_id = m_img.group(1)
                high_res_img = f'https://http2.mlstatic.com/D_NQ_NP_{clean_img_id}-O.jpg'

            if item_id not in results:
                results[item_id] = {
                    'id': item_id,
                    'title': title,
                    'price': price,
                    'link': link,
                    'img_thumb': img_src,
                    'img_high_res': high_res_img,
                    'category': category
                }
    return results

inbrima_items = extract_items(inbrima_files, 'inbrima')
roly_items = extract_items(roly_files, 'roly_toys')

print(f'Total Matchbox Inbrima items found: {len(inbrima_items)}')
print(f'Total Matchbox Roly Toys items found: {len(roly_items)}')

with open('catalog.json', 'w', encoding='utf-8') as f:
    json.dump({'inbrima': list(inbrima_items.values()), 'roly_toys': list(roly_items.values())}, f, ensure_ascii=False, indent=2)

print('Saved catalog.json')
