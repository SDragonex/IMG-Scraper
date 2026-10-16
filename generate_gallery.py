import json
import os
import html

BASE_DIR = r"c:\Users\d.chaker\Documents\antigravity\zealous-hopper"
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
CATALOG_PATH = os.path.join(DOWNLOADS_DIR, "models_catalog.json")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    cat = json.load(f)

inbrima_items = cat.get("inbrima", [])
roly_items = cat.get("roly_toys", [])

multi_roly = sum(1 for it in roly_items if len(it.get("photos", [])) > 1)
multi_inbrima = sum(1 for it in inbrima_items if len(it.get("photos", [])) > 1)
total_multi = multi_roly + multi_inbrima
total_photos = sum(len(it.get("photos", [])) for it in roly_items + inbrima_items)

def generate_html(is_root=True):
    path_prefix = "downloads/" if is_root else ""
    csv_link = "downloads/models_catalog.csv" if is_root else "models_catalog.csv"
    json_link = "downloads/models_catalog.json" if is_root else "models_catalog.json"

    content = f"""<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matchbox Inbrima & Roly Toys - Kompletní HD Fotogalerie</title>
    <style>
        :root {{
            --bg-color: #0b1120;
            --surface: #1e293b;
            --surface-card: #1e293b;
            --card-border: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0284c7;
            --tag-inbrima: #10b981;
            --tag-roly: #f59e0b;
            --tag-multi: #6366f1;
            --btn-dl: #059669;
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 24px;
        }}
        header {{
            max-width: 1440px;
            margin: 0 auto 24px auto;
            background: var(--surface);
            padding: 28px;
            border-radius: 16px;
            border: 1px solid var(--card-border);
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 12px;
        }}
        h1 {{
            margin: 0;
            font-size: 32px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .export-buttons {{
            display: flex;
            gap: 10px;
        }}
        .export-btn {{
            background: #0f172a;
            color: #38bdf8;
            border: 1px solid #38bdf8;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .export-btn:hover {{
            background: #38bdf8;
            color: #0f172a;
        }}
        p.subtitle {{
            margin: 0 0 20px 0;
            color: var(--text-muted);
            font-size: 15px;
            line-height: 1.5;
        }}
        .stats-badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 22px;
        }}
        .stat-pill {{
            background: #0f172a;
            border: 1px solid var(--card-border);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            color: #cbd5e1;
        }}
        .stat-pill b {{
            color: var(--accent);
        }}
        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
        }}
        .search-box {{
            flex: 1;
            min-width: 260px;
            padding: 12px 18px;
            border: 1px solid var(--card-border);
            border-radius: 10px;
            background: #0f172a;
            color: #fff;
            font-size: 15px;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-box:focus {{
            border-color: var(--accent);
        }}
        .filter-btn {{
            padding: 10px 18px;
            border: 1px solid var(--card-border);
            border-radius: 10px;
            background: #0f172a;
            color: #e2e8f0;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
        }}
        .filter-btn:hover {{
            background: #334155;
        }}
        .filter-btn.active {{
            background: var(--accent);
            color: #0f172a;
            border-color: var(--accent);
        }}
        .toggle-gallery-btn {{
            padding: 10px 18px;
            border: 1px solid var(--tag-multi);
            border-radius: 10px;
            background: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
        }}
        .toggle-gallery-btn.active {{
            background: var(--tag-multi);
            color: #fff;
        }}
        .grid {{
            max-width: 1440px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 22px;
        }}
        .card {{
            background: var(--surface-card);
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid var(--card-border);
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
        }}
        .card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.5);
            border-color: #475569;
        }}
        .card-img-container {{
            position: relative;
            width: 100%;
            height: 250px;
            background: #020617;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            user-select: none;
        }}
        .card-img-container img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 8px;
            transition: transform 0.2s;
            cursor: pointer;
        }}
        .card-img-container:hover img {{
            transform: scale(1.03);
        }}
        .carousel-btn {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(15, 23, 42, 0.8);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.2);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            opacity: 0;
            transition: opacity 0.2s, background 0.2s;
            z-index: 5;
        }}
        .card-img-container:hover .carousel-btn {{
            opacity: 1;
        }}
        .carousel-btn:hover {{
            background: var(--accent);
            color: #0f172a;
        }}
        .carousel-btn.prev {{ left: 8px; }}
        .carousel-btn.next {{ right: 8px; }}
        .badge-cat {{
            position: absolute;
            top: 10px;
            left: 10px;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            z-index: 4;
            box-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }}
        .badge-inbrima {{ background: var(--tag-inbrima); }}
        .badge-roly {{ background: var(--tag-roly); }}
        .badge-photos-count {{
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(4px);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.4);
            z-index: 4;
        }}
        .card-body {{
            padding: 16px;
            display: flex;
            flex-direction: column;
            flex: 1;
        }}
        .card-title {{
            font-size: 15px;
            font-weight: 600;
            color: #f1f5f9;
            margin: 0 0 14px 0;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            height: 42px;
        }}
        .card-footer {{
            margin-top: auto;
            display: flex;
            gap: 8px;
        }}
        .btn-view-gallery {{
            flex: 1;
            padding: 9px 12px;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s;
        }}
        .btn-view-gallery:hover {{
            background: var(--accent);
            color: #0f172a;
        }}
        .btn-card-dl {{
            padding: 9px 12px;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }}
        .btn-card-dl:hover {{
            background: #10b981;
            color: #0f172a;
        }}
        .btn-ml-link {{
            padding: 9px 12px;
            background: #0f172a;
            color: #94a3b8;
            border: 1px solid var(--card-border);
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }}
        .btn-ml-link:hover {{
            color: #fff;
            border-color: #64748b;
        }}

        /* Lightbox Modal */
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(5, 10, 20, 0.96);
            backdrop-filter: blur(10px);
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 16px;
        }}
        .modal.active {{
            display: flex;
        }}
        .modal-header {{
            width: 100%;
            max-width: 1200px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            color: #fff;
            gap: 16px;
        }}
        .modal-title-box {{
            flex: 1;
            min-width: 0;
        }}
        .modal-title {{
            font-size: 18px;
            font-weight: 700;
            color: #f8fafc;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .modal-counter {{
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 4px;
        }}
        .modal-toolbar {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .toolbar-btn {{
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid var(--card-border);
            color: #e2e8f0;
            padding: 7px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .toolbar-btn:hover {{
            background: var(--accent);
            color: #0f172a;
            border-color: var(--accent);
        }}
        .toolbar-btn.active {{
            background: var(--accent);
            color: #0f172a;
        }}
        .modal-close {{
            background: none;
            border: none;
            color: #94a3b8;
            font-size: 26px;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            transition: color 0.2s;
            line-height: 1;
        }}
        .modal-close:hover {{ color: #fff; }}
        
        .modal-content-area {{
            position: relative;
            width: 100%;
            max-width: 1200px;
            height: 72vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: #020617;
            border-radius: 12px;
            border: 1px solid var(--card-border);
        }}
        .modal-content-area.zoom-active {{
            overflow: auto;
            cursor: grab;
            display: block;
            text-align: center;
        }}
        .modal-img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 6px;
            cursor: zoom-in;
            user-select: none;
            transition: transform 0.2s;
        }}
        .modal-img.zoomed-100 {{
            max-width: none;
            max-height: none;
            cursor: zoom-out;
            margin: auto;
        }}
        .modal-nav-btn {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid var(--card-border);
            color: #fff;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 24px;
            transition: all 0.2s;
            z-index: 10;
        }}
        .modal-nav-btn:hover {{
            background: var(--accent);
            color: #0f172a;
        }}
        .modal-nav-btn.prev {{ left: 14px; }}
        .modal-nav-btn.next {{ right: 14px; }}
        
        .modal-thumbnails {{
            width: 100%;
            max-width: 1200px;
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding: 12px 0 4px 0;
            justify-content: center;
        }}
        .modal-thumb {{
            width: 72px;
            height: 54px;
            object-fit: cover;
            border-radius: 6px;
            border: 2px solid transparent;
            cursor: pointer;
            background: #000;
            opacity: 0.6;
            transition: all 0.2s;
            flex-shrink: 0;
        }}
        .modal-thumb:hover {{ opacity: 0.9; }}
        .modal-thumb.active {{
            border-color: var(--accent);
            opacity: 1;
            transform: scale(1.05);
        }}

        /* Scroll to top */
        .btn-scroll-top {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 44px;
            height: 44px;
            background: var(--surface);
            border: 1px solid var(--card-border);
            color: #38bdf8;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            opacity: 0;
            visibility: hidden;
            transition: all 0.2s;
            z-index: 90;
        }}
        .btn-scroll-top.visible {{
            opacity: 1;
            visibility: visible;
        }}
        .btn-scroll-top:hover {{
            background: var(--accent);
            color: #0f172a;
        }}
    </style>
</head>
<body>

<header>
    <div class="header-top">
        <h1>🚗 Matchbox Inbrima & Roly Toys</h1>
        <div class="export-buttons">
            <a href="{csv_link}" download class="export-btn" title="Stáhnout celou databázi v CSV">📥 Stáhnout CSV</a>
            <a href="{json_link}" download class="export-btn" title="Stáhnout kompletní JSON metadata">📥 Stáhnout JSON</a>
        </div>
    </div>
    <p class="subtitle">Kompletní HD fotokatalog vzácných brazilských modelů z Mercado Livre Brasil. Všechny fotografie staženy ve 100% plném rozlišení (1200px) s možností lupy na vyražené nápisy podvozku (baseplate).</p>
    
    <div class="stats-badge-row">
        <div class="stat-pill">Celkem v katalogu: <b>{len(inbrima_items) + len(roly_items)} modelů</b></div>
        <div class="stat-pill">S kompletní HD galerií: <b>{total_multi} inzerátů</b></div>
        <div class="stat-pill">HD fotografií na disku: <b>{total_photos} foto</b></div>
        <div class="stat-pill">Matchbox Roly Toys: <b>{len(roly_items)} modelů</b> (100% full gallery)</div>
        <div class="stat-pill">Matchbox Inbrima: <b>{len(inbrima_items)} modelů</b> ({multi_inbrima} s full gallery)</div>
    </div>

    <div class="controls">
        <input type="text" id="searchInput" class="search-box" placeholder="Hledat model (např. Scania, Interlagos, Bora, Corvette, DKW, Kombi, Mercedes, Crane, Tractor...)" onkeyup="filterCards()">
        <button class="filter-btn active" id="btn-all" onclick="setCategory('all')">Všechny ({len(inbrima_items) + len(roly_items)})</button>
        <button class="filter-btn" id="btn-roly_toys" onclick="setCategory('roly_toys')">Matchbox Roly Toys ({len(roly_items)})</button>
        <button class="filter-btn" id="btn-inbrima" onclick="setCategory('inbrima')">Matchbox Inbrima ({len(inbrima_items)})</button>
        <button class="toggle-gallery-btn" id="btn-only-multi" onclick="toggleMultiOnly()">Pouze s kompletní HD galerií ({total_multi})</button>
    </div>
    <div style="margin-top: 14px; font-size: 14px; color: var(--text-muted);" id="statsCount">Zobrazeno {len(inbrima_items) + len(roly_items)} modelů</div>
</header>

<div class="grid" id="cardsGrid">
"""

    def make_card(item, idx, category, badge_class, badge_label):
        title = html.escape(item.get("title", ""))
        link = html.escape(item.get("link", ""))
        photos = item.get("photos", [])
        
        if not photos:
            loc = item.get("local_file", "")
            img_rel = os.path.basename(loc) if loc else ""
            subfolder = "matchbox_inbrima" if category == "inbrima" else "matchbox_roly_toys"
            if img_rel:
                photos = [f"{subfolder}/{img_rel}"]
            elif item.get("img_high_res"):
                photos = [item.get("img_high_res")]
            else:
                photos = [item.get("img_thumb", "")]
                
        # Adjust path prefix for root vs downloads/
        adjusted_photos = []
        for p in photos:
            if p.startswith("http"):
                adjusted_photos.append(p)
            else:
                adjusted_photos.append(f"{path_prefix}{p}")
                
        num_photos = len(adjusted_photos)
        photos_json = html.escape(json.dumps(adjusted_photos))
        first_photo = adjusted_photos[0] if adjusted_photos else ""
        
        has_multi = "true" if num_photos > 1 else "false"
        multi_badge = f'<span class="badge-photos-count">📷 {num_photos} HD fotek</span>' if num_photos > 1 else '<span class="badge-photos-count">📷 1 foto</span>'

        return f"""
        <div class="card" id="card-{category}-{idx}" data-category="{category}" data-title="{title.lower()}" data-multi="{has_multi}" data-photos='{photos_json}' data-item-title="{title}" data-item-link="{link}">
            <div class="card-img-container" id="imgbox-{category}-{idx}">
                <span class="badge-cat {badge_class}">{badge_label}</span>
                {multi_badge}
                <img src="{first_photo}" alt="{title}" id="card-img-{category}-{idx}" loading="lazy" onclick="openLightbox('{category}', {idx}, 0)">
                {f'<button class="carousel-btn prev" onclick="prevCardPhoto(\'{category}\', {idx}, event)">❮</button>' if num_photos > 1 else ''}
                {f'<button class="carousel-btn next" onclick="nextCardPhoto(\'{category}\', {idx}, event)">❯</button>' if num_photos > 1 else ''}
            </div>
            <div class="card-body">
                <div class="card-title" title="{title}">{title}</div>
                <div class="card-footer">
                    <button class="btn-view-gallery" onclick="openLightbox('{category}', {idx}, 0)">Prohlédnout HD ({num_photos})</button>
                    <a href="{first_photo}" download id="dl-btn-{category}-{idx}" class="btn-card-dl" title="Stáhnout aktuální fotografii">⬇</a>
                    <a href="{link}" target="_blank" class="btn-ml-link" rel="noopener noreferrer" title="Původní inzerát na Mercado Livre">ML ↗</a>
                </div>
            </div>
        </div>
        """

    # Add Roly Toys cards first
    for idx, item in enumerate(roly_items):
        content += make_card(item, idx, "roly_toys", "badge-roly", "Roly Toys")

    # Add Inbrima cards
    for idx, item in enumerate(inbrima_items):
        content += make_card(item, idx, "inbrima", "badge-inbrima", "Inbrima")

    content += """
</div>

<!-- Scroll to top button -->
<button class="btn-scroll-top" id="btnScrollTop" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="Zpět nahoru">▲</button>

<!-- Lightbox Modal -->
<div class="modal" id="lightboxModal" onclick="closeLightbox(event)">
    <div class="modal-header" onclick="event.stopPropagation()">
        <div class="modal-title-box">
            <div class="modal-title" id="modalTitle">Název modelu</div>
            <div class="modal-counter" id="modalCounter">Foto 1 z 10</div>
        </div>
        <div class="modal-toolbar">
            <button class="toolbar-btn" id="btnZoom" onclick="toggleZoom()" title="Klikněte pro 100% zobrazení pixelů (skvělé pro baseplate)">🔍 100% Lupa (Baseplate)</button>
            <a href="" target="_blank" id="btnOpenFull" class="toolbar-btn" title="Otevřít originální soubor v plném rozlišení v nové záložce">↗ Originál HD</a>
            <a href="" download id="btnModalDownload" class="toolbar-btn" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border-color: #10b981;" title="Stáhnout fotografii v plné kvalitě">⬇ Stáhnout foto</a>
            <button class="modal-close" onclick="closeLightbox(event)">✕</button>
        </div>
    </div>
    <div class="modal-content-area" id="modalContentArea" onclick="handleAreaClick(event)">
        <button class="modal-nav-btn prev" onclick="prevModalPhoto(event)">❮</button>
        <img class="modal-img" id="modalImg" src="" alt="Detail modelu" onclick="toggleZoom()">
        <button class="modal-nav-btn next" onclick="nextModalPhoto(event)">❯</button>
    </div>
    <div class="modal-thumbnails" id="modalThumbnails" onclick="event.stopPropagation()"></div>
</div>

<script>
let currentCategory = 'all';
let showOnlyMulti = false;
let activeModalPhotos = [];
let activeModalIndex = 0;
let cardPhotoIndices = {};
let isZoomed = false;

function setCategory(cat) {
    currentCategory = cat;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    const btn = document.getElementById('btn-' + cat) || document.getElementById('btn-' + cat.replace('_toys', ''));
    if (btn) btn.classList.add('active');
    filterCards();
}

function toggleMultiOnly() {
    showOnlyMulti = !showOnlyMulti;
    const btn = document.getElementById('btn-only-multi');
    if (showOnlyMulti) {
        btn.classList.add('active');
    } else {
        btn.classList.remove('active');
    }
    filterCards();
}

function filterCards() {
    const query = document.getElementById('searchInput').value.toLowerCase().trim();
    const cards = document.querySelectorAll('.card');
    let visibleCount = 0;
    
    cards.forEach(card => {
        const cat = card.getAttribute('data-category');
        const title = card.getAttribute('data-title');
        const isMulti = card.getAttribute('data-multi') === 'true';
        
        const catMatch = (currentCategory === 'all' || cat === currentCategory);
        const searchMatch = !query || title.includes(query);
        const multiMatch = !showOnlyMulti || isMulti;
        
        if (catMatch && searchMatch && multiMatch) {
            card.style.display = 'flex';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    document.getElementById('statsCount').innerText = `Zobrazeno ${visibleCount} z ${cards.length} modelů`;
}

function prevCardPhoto(category, idx, event) {
    event.stopPropagation();
    const key = `${category}-${idx}`;
    const card = document.getElementById(`card-${key}`);
    const photos = JSON.parse(card.getAttribute('data-photos'));
    let cur = cardPhotoIndices[key] || 0;
    cur = (cur - 1 + photos.length) % photos.length;
    cardPhotoIndices[key] = cur;
    document.getElementById(`card-img-${key}`).src = photos[cur];
    document.getElementById(`dl-btn-${key}`).href = photos[cur];
    updateCardBadge(card, cur, photos.length);
}

function nextCardPhoto(category, idx, event) {
    event.stopPropagation();
    const key = `${category}-${idx}`;
    const card = document.getElementById(`card-${key}`);
    const photos = JSON.parse(card.getAttribute('data-photos'));
    let cur = cardPhotoIndices[key] || 0;
    cur = (cur + 1) % photos.length;
    cardPhotoIndices[key] = cur;
    document.getElementById(`card-img-${key}`).src = photos[cur];
    document.getElementById(`dl-btn-${key}`).href = photos[cur];
    updateCardBadge(card, cur, photos.length);
}

function updateCardBadge(card, curIndex, total) {
    const badge = card.querySelector('.badge-photos-count');
    if (badge && total > 1) {
        badge.innerText = `📷 ${curIndex + 1} / ${total} HD`;
    }
}

function openLightbox(category, idx, photoIndex) {
    const key = `${category}-${idx}`;
    const card = document.getElementById(`card-${key}`);
    activeModalPhotos = JSON.parse(card.getAttribute('data-photos'));
    activeModalIndex = photoIndex || cardPhotoIndices[key] || 0;
    
    document.getElementById('modalTitle').innerText = card.getAttribute('data-item-title');
    document.getElementById('lightboxModal').classList.add('active');
    
    resetZoom();
    renderModalPhoto();
}

function renderModalPhoto() {
    if (!activeModalPhotos || activeModalPhotos.length === 0) return;
    const curSrc = activeModalPhotos[activeModalIndex];
    document.getElementById('modalImg').src = curSrc;
    document.getElementById('modalCounter').innerText = `HD Fotografie ${activeModalIndex + 1} z ${activeModalPhotos.length}`;
    document.getElementById('btnOpenFull').href = curSrc;
    document.getElementById('btnModalDownload').href = curSrc;
    
    resetZoom();

    // Render thumbs
    const thumbsContainer = document.getElementById('modalThumbnails');
    thumbsContainer.innerHTML = '';
    activeModalPhotos.forEach((src, i) => {
        const img = document.createElement('img');
        img.src = src;
        img.className = 'modal-thumb' + (i === activeModalIndex ? ' active' : '');
        img.onclick = (e) => {
            e.stopPropagation();
            activeModalIndex = i;
            renderModalPhoto();
        };
        thumbsContainer.appendChild(img);
    });
}

function toggleZoom() {
    isZoomed = !isZoomed;
    const img = document.getElementById('modalImg');
    const area = document.getElementById('modalContentArea');
    const btn = document.getElementById('btnZoom');
    
    if (isZoomed) {
        img.classList.add('zoomed-100');
        area.classList.add('zoom-active');
        btn.classList.add('active');
        btn.innerText = '🔍 Oddálit (Fit)';
    } else {
        resetZoom();
    }
}

function resetZoom() {
    isZoomed = false;
    const img = document.getElementById('modalImg');
    const area = document.getElementById('modalContentArea');
    const btn = document.getElementById('btnZoom');
    if (img) img.classList.remove('zoomed-100');
    if (area) area.classList.remove('zoom-active');
    if (btn) {
        btn.classList.remove('active');
        btn.innerText = '🔍 100% Lupa (Baseplate)';
    }
}

function handleAreaClick(event) {
    if (event.target === document.getElementById('modalContentArea')) {
        toggleZoom();
    }
}

function prevModalPhoto(event) {
    if (event) event.stopPropagation();
    if (!activeModalPhotos || activeModalPhotos.length <= 1) return;
    activeModalIndex = (activeModalIndex - 1 + activeModalPhotos.length) % activeModalPhotos.length;
    renderModalPhoto();
}

function nextModalPhoto(event) {
    if (event) event.stopPropagation();
    if (!activeModalPhotos || activeModalPhotos.length <= 1) return;
    activeModalIndex = (activeModalIndex + 1) % activeModalPhotos.length;
    renderModalPhoto();
}

function closeLightbox(event) {
    if (event) event.stopPropagation();
    document.getElementById('lightboxModal').classList.remove('active');
    resetZoom();
}

// Keyboard navigation
window.addEventListener('keydown', (e) => {
    const modal = document.getElementById('lightboxModal');
    if (modal.classList.contains('active')) {
        if (e.key === 'ArrowLeft') prevModalPhoto();
        if (e.key === 'ArrowRight') nextModalPhoto();
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'z' || e.key === 'Z') toggleZoom();
    }
});

// Scroll to top button visibility
window.addEventListener('scroll', () => {
    const btn = document.getElementById('btnScrollTop');
    if (window.scrollY > 400) {
        btn.classList.add('visible');
    } else {
        btn.classList.remove('visible');
    }
});
</script>

</body>
</html>
"""
    return content

# 1. Generate root index.html (for https://sdragonex.github.io/IMG-Scraper/)
root_index_path = os.path.join(BASE_DIR, "index.html")
with open(root_index_path, "w", encoding="utf-8") as f:
    f.write(generate_html(is_root=True))

# 2. Generate downloads/index.html (for local browsing in downloads folder)
downloads_index_path = os.path.join(DOWNLOADS_DIR, "index.html")
with open(downloads_index_path, "w", encoding="utf-8") as f:
    f.write(generate_html(is_root=False))

print(f"Generated root index.html (clean GitHub Pages URL): {root_index_path}")
print(f"Generated downloads/index.html (local folder): {downloads_index_path}")
print(f"Total listings: {len(inbrima_items) + len(roly_items)}")
print(f"Listings with full multi-image gallery: {total_multi}")
print(f"Total photos linked: {total_photos}")
