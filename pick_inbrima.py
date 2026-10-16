import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\d.chaker\Documents\antigravity\zealous-hopper\downloads\models_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

# Pick distinct models by casting/name
seen_names = set()
selected = []
for it in cat['inbrima']:
    t = it['title']
    # Extract simple model key
    words = t.split()
    key = ' '.join(words[:5])
    if key not in seen_names:
        seen_names.add(key)
        clean_link = it['link'].split('#')[0]
        selected.append((it['id'], clean_link, t))
    if len(selected) >= 30:
        break

for i, (item_id, link, title) in enumerate(selected, 1):
    print(f"{i}|{item_id}|{link}|{title}")
