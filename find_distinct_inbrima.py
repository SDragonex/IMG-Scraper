import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('downloads/models_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

inbrima = cat['inbrima']

items = []
for it in inbrima:
    t = it['title']
    tl = t.lower()
    if 'majorette' in tl:
        continue
    items.append(it)

print(f"Total Matchbox Inbrima items: {len(items)}")

seen_models = {}
for it in items:
    t = it['title']
    clean = re.sub(r'(?i)(inbrima|imbrima|matchbox|miniatura|carrinho|caminhao|caminhão|superfast|speed kings|rolamatics|prod|z\.f|manaus|brasil|raro|antigo|lote|blister|caixa|b\d{3,4})', '', t)
    clean = ' '.join(clean.split())
    words = [w for w in clean.split() if len(w) > 1][:3]
    key = ' '.join(words).lower()
    if key and key not in seen_models:
        seen_models[key] = it

print(f"Unique casting keys identified: {len(seen_models)}")

# Also let's see which ones we already fetched:
already_fetched_ids = {
    'MLB3837203209', 'MLB4227105723', 'MLB4001339406', 'MLB5347328079',
    'MLB5347306017', 'MLB7764902866', 'MLB5325058193', 'MLB5325044077',
    'MLB7702025880', 'MLB5347132051', 'MLB7763743306'
}

candidates = []
for k, it in seen_models.items():
    if it['id'] not in already_fetched_ids:
        candidates.append((k, it))

print(f"Remaining candidates to fetch: {len(candidates)}")
for i, (k, it) in enumerate(candidates[:20], 1):
    link = it['link'].split('#')[0]
    print(f"{i}|{it['id']}|{link}|{it['title']}")
