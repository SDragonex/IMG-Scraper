# Matchbox Inbrima & Matchbox Roly Toys – Fotokatalog (Mercado Livre Brasil)

Kompletní archiv a vizuální katalog vzácných brazilských modelů autíček **Matchbox Inbrima** (Zona Franca de Manaus) a **Matchbox Roly Toys** (Rio de Janeiro) vyhledaných na brazilském tržišti Mercado Livre.

Projekt obsahuje:
- **309 celkových nabídek** s cenami, názvy a původními odkazy.
- **50 kompletních vícesnímkových fotogalerií** (566 fotografií ve vysokém rozlišení).
- Fotografie detailů: přední/zadní pohled, podvozek/baseplate (s vyraženými značkami Inbrima Manaus / Roly Toys), boky a originální obaly/krabičky.
- Interaktivní webovou galerii `index.html` s karuselem, lightboxem a vyhledáváním.
- Exporty v formátech JSON a CSV.

---

## 🚀 Jak spustit lokálně
Jednoduše otevřete v prohlížeči soubor `downloads/index.html` (nebo kořenový `index.html`).

---

## 📁 Struktura projektu
```text
├── index.html                   # Přesměrování na galerii (vhodné pro GitHub Pages)
├── downloads/
│   ├── index.html               # Interaktivní webová galerie
│   ├── models_catalog.json      # Kompletní JSON databáze modelů a fotek
│   ├── models_catalog.csv       # Tabulkový export (Excel / Google Sheets)
│   ├── matchbox_roly_toys/      # Fotografie modelů Roly Toys
│   └── matchbox_inbrima/        # Fotografie modelů Inbrima
└── *.py                         # Skripty pro scraping, stahování a generování
```

---

## 🌐 Publikace na GitHub & GitHub Pages
Celá složka `downloads/` má velikost pouze **~21.6 MB**, takže ji lze přímo nahrát do běžného GitHub repozitáře bez nutnosti Git LFS:

```bash
git add .
git commit -m "Add Matchbox Inbrima & Roly Toys photo catalog"
git branch -M main
git remote add origin https://github.com/<vase-uzivatelske-jmeno>/<nazev-repozitare>.git
git push -u origin main
```

Pro aktivaci živé webové stránky zdarma:
1. Přejděte v repozitáři na GitHubu do **Settings** -> **Pages**.
2. V sekci **Build and deployment** zvolte:
   - Source: **Deploy from a branch**
   - Branch: **main** / **root** (`/`)
3. Během minuty bude web dostupný online na adrese `https://<vase-uzivatelske-jmeno>.github.io/<nazev-repozitare>/`.
