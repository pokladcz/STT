import os
import json

path = r"C:\Users\pokla\STT-fork\site-structure.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Add our new interactive lesson to Robotika
data["robotikaCards"].insert(0, {
    "id": "robotika",
    "title": "Interaktivní úvod do Robotiky (Ukázka)",
    "href": "interaktivni-uvod/index.html",
    "status": "ready"
})

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Added interactive lesson to Robotika.")
