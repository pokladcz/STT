import json
import os

path = r"C:\Users\pokla\STT-fork\site-structure.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["home"] = {
    "cards": [
        {
            "id": "stt",
            "title": "STT (Strojírenská technologie)",
            "href": "stt/index.html",
            "status": "ready"
        },
        {
            "id": "sps",
            "title": "SPS (Stavba a provoz strojů)",
            "href": "sps/index.html",
            "status": "ready"
        },
        {
            "id": "mec",
            "title": "MEC (Mechanika)",
            "href": "mec/index.html",
            "status": "ready"
        },
        {
            "id": "robotika",
            "title": "Robotika",
            "href": "robotika/index.html",
            "status": "ready"
        },
        {
            "id": "cnc",
            "title": "CNC Programování",
            "href": "cnc/index.html",
            "status": "ready"
        },
        {
            "id": "mte",
            "title": "MTE (Měření a testování)",
            "href": "mte/index.html",
            "status": "ready"
        }
    ]
}

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON updated successfully.")
