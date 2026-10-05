import os
import codecs

base_dir = r"C:\Users\pokla\STT-fork"

def fix_fetch(filepath):
    if not os.path.exists(filepath):
        return
    with codecs.open(filepath, "r", "utf-8") as f:
        html = f.read()
    
    # Add cache buster to the fetch call
    html = html.replace("fetch('site-structure.json')", "fetch('site-structure.json?v=' + new Date().getTime())")
    html = html.replace("fetch('../site-structure.json')", "fetch('../site-structure.json?v=' + new Date().getTime())")
    
    with codecs.open(filepath, "w", "utf-8") as f:
        f.write(html)

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            fix_fetch(os.path.join(root, file))

print("Cache busting added to all HTML files.")
