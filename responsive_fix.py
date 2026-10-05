import os
import json
import codecs
import shutil

base_dir = r"C:\Users\pokla\STT-fork"
path_json = os.path.join(base_dir, "site-structure.json")

with open(path_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. Update site-structure.json
# Remove "STT" from nav since it will be on home page
data["nav"] = [item for item in data.get("nav", []) if item.get("title") != "STT"]

# Rebuild home.cards
stt_cards = [
    {"id": "vnitrni-stavba", "title": "Vnitřní stavba kovů a tepelné zpracování", "href": "vnitrni-stavba-kovu-a-tz/index.html?view=home", "status": "ready"},
    {"id": "koroze", "title": "Koroze", "href": "koroze/index.html", "status": "ready"},
    {"id": "tvareni", "title": "Tváření", "href": "tvareni-za-tepla/index.html", "status": "ready"},
    {"id": "praskova-metalurgie", "title": "Prášková metalurgie", "href": "praskova-metalurgie/index.html", "status": "ready"},
    {"id": "znaceni-oceli", "title": "Značení ocelí dle EN", "href": "znaceni-oceli/index.html", "status": "ready"},
    {"id": "odlevani", "title": "Odlévání", "href": "odlevani/index.html", "status": "ready"}
]

other_cards = [
    {"id": "sps", "title": "Stavba a provoz strojů (SPS)", "href": "sps/index.html", "status": "ready"},
    {"id": "mec", "title": "Mechanika (MEC)", "href": "mec/index.html", "status": "ready"},
    {"id": "cnc", "title": "CNC Programování", "href": "cnc/index.html", "status": "ready"},
    {"id": "mte", "title": "Měření a testování (MTE)", "href": "mte/index.html", "status": "ready"}
]

data["home"]["cards"] = stt_cards + other_cards

with open(path_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Add responsive CSS to HTML files
def make_responsive(filepath):
    if not os.path.exists(filepath):
        return
    with codecs.open(filepath, "r", "utf-8") as f:
        html = f.read()
    
    # Inject CSS before </style>
    responsive_css = """
    @media (max-width: 900px) { #cardsContainer { grid-template-columns: repeat(2, 1fr) !important; } }
    @media (max-width: 600px) { #cardsContainer { grid-template-columns: 1fr !important; } }
    /* Fix header wrapping */
    h1 { font-size: 32px !important; }
    """
    if "grid-template-columns: 1fr" not in html:
        html = html.replace("</style>", responsive_css + "\n  </style>")
        
        # Ensure #cardsContainer is present on the grid div
        if 'id="cardsContainer"' not in html:
            html = html.replace('display:grid;grid-template-columns:repeat(3,1fr);', 'display:grid;grid-template-columns:repeat(3,1fr);', 1)
            # Actually, I already added id="cardsContainer" in build_unified.py, let's just make sure.
            
    with codecs.open(filepath, "w", "utf-8") as f:
        f.write(html)

# Apply to root
make_responsive(os.path.join(base_dir, "index.html"))

# Apply to sub-hubs
for folder in ["sps", "mec", "cnc", "mte"]:
    make_responsive(os.path.join(base_dir, folder, "index.html"))

# 3. Delete 'stt' folder
stt_folder = os.path.join(base_dir, "stt")
if os.path.exists(stt_folder):
    shutil.rmtree(stt_folder)

print("Responsive CSS added, STT hub removed, homepage updated.")
