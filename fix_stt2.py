import subprocess

# get raw content from git
result = subprocess.run(["git", "show", "677e60ac5c1b0a3f1af2a5d8710c356b6343a488:index.html"], capture_output=True)
content = result.stdout.decode('utf-8')

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

with open(r"C:\Users\pokla\STT-fork\stt\index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed stt/index.html")
