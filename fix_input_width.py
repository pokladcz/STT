import os
import codecs

repo_dir = r"C:\Users\pokla\STT-fork"
files = ["index.html", "stt/index.html", "sps/index.html", "mec/index.html", "cnc/index.html", "mte/index.html"]

for rel in files:
    path = os.path.join(repo_dir, rel)
    if not os.path.exists(path): continue
    
    with codecs.open(path, "r", "utf-8") as f:
        html = f.read()
        
    html = html.replace('<div style="margin-bottom: 32px;">\n      <input type="text" id="searchInput"', 
                        '<div style="margin-bottom: 32px; max-width: 500px;">\n      <input type="text" id="searchInput"')
                        
    with codecs.open(path, "w", "utf-8") as f:
        f.write(html)
