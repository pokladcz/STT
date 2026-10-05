import json
import os

path = r"C:\Users\pokla\STT-fork\site-structure.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. Remove Robotika from nav
data["nav"] = [item for item in data.get("nav", []) if item.get("title") not in ["ROBOTIKA", "Robotika"]]

# 2. Remove Robotika from home.cards
if "home" in data and "cards" in data["home"]:
    data["home"]["cards"] = [card for card in data["home"]["cards"] if card.get("id") != "robotika"]

# 3. Fix URLs in sttCards to go up one level so they hit the root folders
for card in data.get("sttCards", []):
    if not card["href"].startswith("../"):
        card["href"] = "../" + card["href"]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Fixed site-structure.json")
