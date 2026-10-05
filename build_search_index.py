import os
import json
import re
import fitz # PyMuPDF

repo_dir = r"C:\Users\pokla\STT-fork"
subjects = ['stt', 'sps', 'mec', 'cnc', 'mte']
index_file = os.path.join(repo_dir, "search-index.json")

search_index = []

def clean_text(text):
    # Lowercase and remove extra whitespace
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

for subject in subjects:
    subj_dir = os.path.join(repo_dir, subject)
    if not os.path.exists(subj_dir): continue
    
    for filename in os.listdir(subj_dir):
        if not filename.lower().endswith('.pdf'): continue
        
        filepath = os.path.join(subj_dir, filename)
        title = filename.replace('.pdf', '')
        url = f"{subject}/{filename}" # relative path from root
        
        try:
            doc = fitz.open(filepath)
            full_text = []
            for page in doc:
                full_text.append(page.get_text("text"))
            
            raw_text = " ".join(full_text)
            cleaned = clean_text(raw_text)
            
            search_index.append({
                "title": title,
                "url": url,
                "subject": subject.upper(),
                "content": cleaned
            })
            print(f"Indexed {url}")
        except Exception as e:
            print(f"Failed to index {url}: {e}")

with open(index_file, 'w', encoding='utf-8') as f:
    json.dump(search_index, f, ensure_ascii=False)

print(f"Search index built with {len(search_index)} documents.")
