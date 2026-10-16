import json
from collections import Counter

with open(r'c:\Users\d.chaker\Documents\antigravity\zealous-hopper\downloads\models_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

inbrima = cat['inbrima']
print(f"Total Inbrima items: {len(inbrima)}")

# Check codes like B080, B073, B048 in titles
codes = [item['title'].split()[-1] for item in inbrima if item['title']]
print("Most common title suffixes/codes:", Counter(codes).most_common(10))

# Sample 20 unique model names
models = set()
for item in inbrima:
    t = item['title'].lower()
    for word in ['maserati', 'snorkel', 'corvette', 'mustang', 'ferrari', 'hovercraft', 'shunter', 'londoner', 'ambulance', 'faun', 'weasel', 'mazda', 'datsun', 'holden', 'hairy hustler', 'soopa coopa', 'saviem', 'sambron']:
        if word in t:
            models.add(word)
print("Recognized distinct casting names:", sorted(models))
