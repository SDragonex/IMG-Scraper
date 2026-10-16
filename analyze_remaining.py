import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('downloads/models_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

single = [x for x in cat['inbrima'] if len(x.get('photos', [])) <= 1]
print(f"Total single-photo Inbrima listings: {len(single)}")

by_group = {}
for x in single:
    t = x['title'].lower()
    clean = re.sub(r'b\d{3,4}', '', t)
    clean = re.sub(r'(inbrima|imbrima|matchbox|miniatura|carrinho|caminhao|caminhão|superfast)', '', clean).strip()
    words = [w for w in clean.split() if len(w) > 1]
    key = ' '.join(words[:2]) if words else 'other'
    by_group.setdefault(key, []).append(x)

print(f"Distinct casting groups: {len(by_group)}")
for k, v in list(by_group.items())[:25]:
    sample = v[0]
    clean_link = sample['link'].split('#')[0]
    print(f"  [{len(v)}x] '{k}' -> {sample['id']} | {clean_link}")
