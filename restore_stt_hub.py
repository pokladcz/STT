import os
import json
import codecs

base_dir = r"C:\Users\pokla\STT-fork"
path_json = os.path.join(base_dir, "site-structure.json")

with open(path_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# The 6 specific STT IDs
stt_ids = ["vnitrni-stavba", "koroze", "tvareni", "praskova-metalurgie", "znaceni-oceli", "odlevani"]

# Separate home cards into STT cards and others
current_home_cards = data.get("home", {}).get("cards", [])
new_stt_cards = [c for c in current_home_cards if c.get("id") in stt_ids]
other_cards = [c for c in current_home_cards if c.get("id") not in stt_ids and c.get("id") != "stt"]

# Update sttCards (make sure paths have ../)
data["sttCards"] = new_stt_cards
for card in data["sttCards"]:
    if not card["href"].startswith("../"):
        card["href"] = "../" + card["href"]

# Create the new home cards array
new_home_cards = [
    {"id": "stt", "title": "Strojírenská technologie (STT)", "href": "stt/index.html", "status": "ready"}
] + other_cards

data["home"]["cards"] = new_home_cards

# Add STT back to nav if missing
nav = data.get("nav", [])
if not any(n.get("title") == "STT" for n in nav):
    # Insert right after Domů
    nav.insert(1, {"title": "STT", "href": "stt/index.html"})
    data["nav"] = nav

with open(path_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Now recreate stt/index.html by copying from sps/index.html
sps_path = os.path.join(base_dir, "sps", "index.html")
with codecs.open(sps_path, "r", "utf-8") as f:
    html = f.read()

# Replace SPS specifics with STT specifics
html = html.replace("Stavba a provoz strojů (SPS) | Výukový portál", "Strojírenská technologie (STT) | Výukový portál")
html = html.replace("Výuka: Stavba a provoz strojů (SPS)", "Strojírenská technologie (STT)")
html = html.replace("s.spsCards", "s.sttCards")

os.makedirs(os.path.join(base_dir, "stt"), exist_ok=True)
with codecs.open(os.path.join(base_dir, "stt", "index.html"), "w", "utf-8") as f:
    f.write(html)

print("STT hub restored successfully.")
