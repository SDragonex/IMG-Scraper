import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('downloads/models_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

unfetched = []
for it in cat['inbrima']:
    if it.get('photos_count', 1) <= 1 and 'majorette' not in it['title'].lower():
        unfetched.append(it)

print(f"Total unfetched Matchbox Inbrima items: {len(unfetched)}")
for i, it in enumerate(unfetched[:30], 1):
    link = it['link'].split('#')[0]
    print(f"{i}|{it['id']}|{link}|{it['title']}")
