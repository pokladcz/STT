import os
import json
import codecs

path_json = r"C:\Users\pokla\STT-fork\site-structure.json"
with open(path_json, "r", encoding="utf-8") as f:
    data = json.load(f)

subjects = {
    "robotika": "Robotika",
    "cnc": "CNC Programování",
    "mte": "Měření a testování (MTE)",
    "sps": "Stavba a provoz strojů (SPS)",
    "mec": "Mechanika (MEC)"
}

# 1. Update JSON with cards for each subject based on their files
for folder, title in subjects.items():
    key = folder + "Cards"
    cards = []
    
    # Read files in folder
    folder_path = os.path.join(r"C:\Users\pokla\STT-fork", folder)
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".pdf") or file.endswith(".html") or file.endswith(".docx"):
                if file == "index.html": continue
                
                # Make an interactive-looking card for each file
                cards.append({
                    "id": "doc",
                    "title": file.replace(".pdf", "").replace(".html", "").replace(".docx", "").replace("_", " "),
                    "href": file,
                    "status": "ready"
                })
    
    data[key] = cards

with open(path_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Create index.html for each subject based on stt/index.html
with codecs.open(r"C:\Users\pokla\STT-fork\stt\index.html", "r", "utf-8") as f:
    base_html = f.read()

for folder, title in subjects.items():
    key = folder + "Cards"
    
    # Replace references in the HTML
    html = base_html.replace('Interaktivní výuka STT', f'Výuka: {title}')
    html = html.replace('s.home.cards', f's.{key}')
    html = html.replace('<title>Interaktivní výuka STT | STT</title>', f'<title>{title} | Strojírenství</title>')
    
    # Write to folder
    out_path = os.path.join(r"C:\Users\pokla\STT-fork", folder, "index.html")
    with codecs.open(out_path, "w", "utf-8") as f:
        f.write(html)

print("Hubs generated.")
