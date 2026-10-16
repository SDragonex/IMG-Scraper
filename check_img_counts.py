import re

with open(r'C:\Users\d.chaker\.gemini\antigravity\brain\bbba99da-072a-4764-8b5c-146459d2ce18\.system_generated\steps\8\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

occ = re.findall(r'https://http2\.mlstatic\.com/D_[^\s"\'<>]+', text)
print(f"Total mlstatic image URLs in search page: {len(occ)}")
print(f"Unique image URLs in search page: {len(set(occ))}")

# Check polycard
cards = text.count('class="poly-card')
print(f"Total poly cards: {cards}")
