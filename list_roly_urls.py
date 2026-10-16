import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\d.chaker\Documents\antigravity\zealous-hopper\downloads\models_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

for i, it in enumerate(cat['roly_toys'], 1):
    clean_link = it['link'].split('#')[0]
    print(f"{i}|{it['id']}|{clean_link}|{it['title']}")
