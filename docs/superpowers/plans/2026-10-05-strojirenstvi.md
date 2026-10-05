# Strojírenství Výukový Portál Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the STT repository into a multi-subject portal (Strojírenství) with a subject selection homepage, a global search bar, and imported materials.

**Architecture:** The project uses a custom Python generator (`sync.py`) and JSON configuration (`site-structure.json`). We will restructure the JSON to include top-level subjects, modify the HTML template to serve as a landing hub, inject a simple JavaScript-based global search, and copy the user's data into the repo structure.

**Tech Stack:** Python 3, HTML/JS/CSS, Markdown.

**Spec:** `docs/superpowers/specs/2026-10-05-strojirenstvi-design.md`

## Global Constraints
- Target audience: Střední průmyslová škola a Vyšší odborná škola Brno, Sokolská (teachers and students).
- Subjects to include: STT, SPS, MEC, Robotika, CNC, MTE.
- All original STT materials must remain functional under the STT category.

---

### Task 1: Update README.md

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: None
- Produces: Updated repository documentation

- [ ] **Step 1: Write the updated README.md**

```markdown
# Výukový portál Strojírenství

Tento projekt slouží jako interaktivní výukový portál pro strojírenské předměty na **Střední průmyslová škola a Vyšší odborná škola Brno, Sokolská, příspěvková organizace**. 
Portál je vytvářen pro učitele i studenty.

## Pro studenty
- **Rozcestník:** Na hlavní stránce si vyberte požadovaný předmět (STT, SPS, MEC, Robotika, CNC, MTE).
- **Zobrazení:** Pro nejlepší zážitek u interaktivních diagramů doporučujeme stisknout klávesu **F11** pro zobrazení na celou obrazovku.
- **Vyhledávání:** Využijte vyhledávací pole v horní části pro rychlé nalezení látky.

## Pro učitele
- Portál je ideální pro promítání v hodinách. Interaktivní prvky a diagramy usnadňují vysvětlování komplexních strojírenských postupů.

## Pro přispěvatele
1. Přidejte složku s novými materiály (Markdown, HTML, PDF).
2. Zaregistrujte novou sekci do `site-structure.json`.
3. Spusťte `python sync.py` pro vygenerování menu a statických stránek.
```

- [ ] **Step 2: Commit changes**

```bash
git add README.md
git commit -m "docs: aktualizace README pro SPS a VOS Brno Sokolska"
```

---

### Task 2: Restructure site-structure.json

**Files:**
- Modify: `site-structure.json`

**Interfaces:**
- Consumes: None
- Produces: Hierarchical JSON containing STT, SPS, MEC, Robotika, CNC, MTE as top-level objects.

- [ ] **Step 1: Write validation script (test)**

```python
# test_structure.py
import json

with open("site-structure.json", "r", encoding="utf-8") as f:
    data = json.load(f)

nav = data.get("nav", [])
titles = [item.get("title") for item in nav]
required = ["STT", "SPS", "MEC", "Robotika", "CNC", "MTE"]

missing = [req for req in required if req not in titles]
if missing:
    print(f"FAIL: Missing subjects {missing}")
    exit(1)
print("PASS")
```

- [ ] **Step 2: Run test (should fail)**
Run: `python test_structure.py`
Expected: FAIL

- [ ] **Step 3: Modify site-structure.json**
Add the new top-level categories and move existing items under `STT`.
```json
{
  "nav": [
    {
      "title": "Domů",
      "href": "index.html"
    },
    {
      "title": "STT",
      "href": "stt/index.html",
      "items": [
        { "title": "Vnitřní stavba kovů a TZ", "href": "vnitrni-stavba-kovu-a-tz/index.html" },
        { "title": "Koroze", "href": "koroze/index.html" },
        { "title": "Tváření", "href": "tvareni-za-tepla/index.html" },
        { "title": "Prášková metalurgie", "href": "praskova-metalurgie/index.html" },
        { "title": "Značení ocelí", "href": "znaceni-oceli/index.html" },
        { "title": "Odlévání", "href": "odlevani/index.html" }
      ]
    },
    { "title": "SPS", "href": "sps/index.html" },
    { "title": "MEC", "href": "mec/index.html" },
    { "title": "Robotika", "href": "robotika/index.html" },
    { "title": "CNC", "href": "cnc/index.html" },
    { "title": "MTE", "href": "mte/index.html" }
  ]
}
```
*(Note: Implementer must preserve exact paths for STT children based on original file)*

- [ ] **Step 4: Run test (should pass)**
Run: `python test_structure.py`
Expected: PASS

- [ ] **Step 5: Commit changes**
```bash
git add site-structure.json test_structure.py
git commit -m "feat: pridani strohirenskych predmetu do navigace"
```

---

### Task 3: Setup Index Page (Rozcestník) and Search Bar

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: Target URLs from `site-structure.json`
- Produces: A landing page with tiles for each subject and a search input.

- [ ] **Step 1: Create the visual layout in index.html**
Replace the content of `index.html` with a grid layout and search bar.

```html
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="utf-8">
    <title>Strojírenství - Výukový Portál</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f4f9; }
        header { text-align: center; margin-bottom: 40px; }
        #search { padding: 10px; width: 80%; max-width: 400px; font-size: 16px; margin-top: 20px; }
        .grid { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 200px; text-align: center; text-decoration: none; color: #333; font-weight: bold; font-size: 18px; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); background: #e0f0ff; }
    </style>
</head>
<body>
    <header>
        <h1>Výukový Portál: Strojírenství</h1>
        <p>SPŠ a VOŠ Brno, Sokolská</p>
        <input type="text" id="search" placeholder="Hledat materiály...">
    </header>
    <div class="grid">
        <a href="stt/index.html" class="card">STT</a>
        <a href="sps/index.html" class="card">SPS</a>
        <a href="mec/index.html" class="card">MEC</a>
        <a href="robotika/index.html" class="card">Robotika</a>
        <a href="cnc/index.html" class="card">CNC</a>
        <a href="mte/index.html" class="card">MTE</a>
    </div>
</body>
</html>
```

- [ ] **Step 2: Commit changes**
```bash
git add index.html
git commit -m "feat: rozcestnik predmetu a priprava vyhledavani"
```

---

### Task 4: Import Data from 1-skola

**Files:**
- Create: Subject folders (`sps`, `mec`, `robotika`, `cnc`, `mte`)
- Copy: Files from `C:\Users\pokla\OneDrive - SPŠ a VOŠ Brno, Sokolská, příspěvková organizace\1-skola`

**Interfaces:**
- Consumes: The original files from OneDrive.
- Produces: Populated directories in the STT-fork repository.

- [ ] **Step 1: Write copy script**

```python
# import_data.py
import os
import shutil

src_base = r"C:\Users\pokla\OneDrive - SPŠ a VOŠ Brno, Sokolská, příspěvková organizace\1-skola"
dest_base = os.getcwd()

mappings = {
    "Robotika": "robotika",
    "CNC": "cnc",
    "MTE": "mte",
    "SPS, MEC, CAD": "sps"  # We'll map the combined folder to SPS for now, implementer can adjust
}

for src_folder, dest_folder in mappings.items():
    src_path = os.path.join(src_base, src_folder)
    dest_path = os.path.join(dest_base, dest_folder)
    if os.path.exists(src_path):
        if not os.path.exists(dest_path):
            shutil.copytree(src_path, dest_path)
            print(f"Copied {src_folder} to {dest_folder}")
    else:
        print(f"Source not found: {src_path}")
```

- [ ] **Step 2: Execute script**
Run: `python import_data.py`

- [ ] **Step 3: Generate placeholder indexes for new subjects**
For each new folder (`robotika`, `cnc`, `mte`, `sps`, `mec`), if `index.html` does not exist, create a basic one that links to the copied PDFs/files.

- [ ] **Step 4: Commit changes**
```bash
git add import_data.py robotika/ cnc/ mte/ sps/ mec/
git commit -m "feat: import zdrojovych dat ze skolni slozky"
```
