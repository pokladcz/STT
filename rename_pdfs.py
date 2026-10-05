import os
import re
import shutil
import json
import fitz  # PyMuPDF

source_dir_stt = r"C:\Users\pokla\OneDrive - SPŠ a VOŠ Brno, Sokolská, příspěvková organizace\1-skola\STT, KOM"
repo_dir = r"C:\Users\pokla\STT-fork"
structure_file = os.path.join(repo_dir, "site-structure.json")

subjects = ['stt', 'sps', 'mec', 'cnc', 'mte']

# 1. Copy STT files to stt/
stt_target = os.path.join(repo_dir, 'stt')
os.makedirs(stt_target, exist_ok=True)
if os.path.exists(source_dir_stt):
    for f in os.listdir(source_dir_stt):
        if f.lower().endswith('.pdf'):
            src = os.path.join(source_dir_stt, f)
            dst = os.path.join(stt_target, f)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)

# Function to clean filename
def clean_filename(filename):
    # Remove VY_32_INOVACE_... - 
    name = re.sub(r'^VY_32_INOVACE_[\d\-\s]+-\s*', '', filename)
    name = re.sub(r'^VY 32 INOVACE [\d\-\s]+-\s*', '', name)
    # Remove 1-STROJÍRENSTVÍ - ... - 
    name = re.sub(r'^1-STROJ[IÍ]RENSTV[IÍ]\s*-\s*\d+\s*-\s*', '', name, flags=re.IGNORECASE)
    return name.strip()

# Function to extract title from edupage hash pdfs
def get_title_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        if len(doc) > 0:
            page = doc[0]
            blocks = page.get_text("dict")["blocks"]
            # Try to find the block with the largest font size
            max_size = 0
            title = ""
            for b in blocks:
                if "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            if s["size"] > max_size and s["text"].strip():
                                max_size = s["size"]
                                title = s["text"].strip()
            if title:
                # clean filename characters
                title = re.sub(r'[\\/*?:"<>|]', '', title)
                return title[:50] + ".pdf"
    except Exception as e:
        pass
    return None

rename_map = {} # old_path -> new_path
href_map = {} # old_href -> new_href (for json)

for subject in subjects:
    subj_dir = os.path.join(repo_dir, subject)
    if not os.path.exists(subj_dir): continue
    
    for filename in os.listdir(subj_dir):
        if not filename.lower().endswith('.pdf'): continue
        
        filepath = os.path.join(subj_dir, filename)
        new_name = clean_filename(filename)
        
        if new_name.startswith('httpscloud'):
            # It's an edupage hash, extract title
            extracted = get_title_from_pdf(filepath)
            if extracted:
                new_name = extracted
            else:
                new_name = "Dokument_" + filename[:8] + ".pdf"
                
        # ensure it ends with pdf
        if not new_name.lower().endswith('.pdf'):
            new_name += ".pdf"
            
        if new_name != filename:
            # check collision
            new_filepath = os.path.join(subj_dir, new_name)
            counter = 1
            base, ext = os.path.splitext(new_name)
            while os.path.exists(new_filepath) and new_filepath != filepath:
                new_filepath = os.path.join(subj_dir, f"{base}_{counter}{ext}")
                counter += 1
            
            os.rename(filepath, new_filepath)
            rename_map[filepath] = new_filepath
            href_map[filename] = os.path.basename(new_filepath)

# Update site-structure.json
with open(structure_file, 'r', encoding='utf-8') as f:
    structure = json.load(f)

# Also, if we copied new files to STT, we should add them to sttCards if not there
stt_files = [f for f in os.listdir(stt_target) if f.lower().endswith('.pdf')]
existing_stt_hrefs = [c.get('href') for c in structure.get('sttCards', [])]

for stt_file in stt_files:
    if stt_file not in existing_stt_hrefs:
        # It's a new PDF! Add it to sttCards
        title = stt_file.replace('.pdf', '')
        structure.setdefault('sttCards', []).append({
            "id": "doc",
            "title": title,
            "href": stt_file,
            "target": "_blank",
            "status": "ready"
        })

# Now apply href_map to all cards in structure
for key in structure:
    if 'Cards' in key and isinstance(structure[key], list):
        for card in structure[key]:
            old_href = card.get('href', '')
            # Try matching exactly or decoded
            for old_name, new_name in href_map.items():
                if old_name == old_href or old_name == old_href.replace('%20', ' '):
                    card['href'] = new_name
                    card['title'] = new_name.replace('.pdf', '')
    elif isinstance(structure[key], dict) and 'cards' in structure[key]:
        for card in structure[key]['cards']:
            old_href = card.get('href', '')
            for old_name, new_name in href_map.items():
                if old_name == old_href or old_name == old_href.replace('%20', ' '):
                    card['href'] = new_name
                    card['title'] = new_name.replace('.pdf', '')

with open(structure_file, 'w', encoding='utf-8') as f:
    json.dump(structure, f, indent=2, ensure_ascii=False)

print("Renamed files and updated structure.")
