import os

path = r"C:\Users\pokla\STT-fork\stt\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix paths for being 1 level deep
content = content.replace('"./support.js"', '"../support.js"')
content = content.replace("fetch('site-structure.json')", "fetch('../site-structure.json')")
content = content.replace('href="koroze', 'href="../koroze')
content = content.replace('href="odlevani', 'href="../odlevani')
content = content.replace('href="praskova', 'href="../praskova')
content = content.replace('href="tvareni', 'href="../tvareni')
content = content.replace('href="znaceni', 'href="../znaceni')
content = content.replace('href="vnitrni', 'href="../vnitrni')
content = content.replace('href="./o-projektu', 'href="../o-projektu')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed stt/index.html")
