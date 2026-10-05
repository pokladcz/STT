import os

repo_dir = r"C:\Users\pokla\STT-fork"

# -- STT Animations --
svar_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Svařovací plameny | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; padding: 48px; text-align: center; }
  .box { background: #fff; border: 1px solid #ded3c2; padding: 24px; border-radius: 16px; display: inline-block; max-width: 600px; width:100%; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  .flame { height: 100px; width: 300px; margin: 0 auto; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 50%, #fff 100%); border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; transition: 0.5s; clip-path: polygon(0 20%, 100% 50%, 0 80%); }
  button { padding: 8px 16px; margin: 4px; border-radius: 8px; border: 1px solid #ded3c2; background: #fbf8f3; cursor: pointer; font-family: inherit; font-size: 16px; transition: 0.2s; }
  button:hover { background: #e5ded2; }
</style>
</head>
<body>
  <div class="box">
    <a href="../stt/index.html" style="color:#b0561f; text-decoration:none; font-weight:600; display:block; text-align:left; margin-bottom:16px;">&larr; Zpět</a>
    <h2 style="font-family:'Quicksand';color:#b0561f;">Druhy svařovacích plamenů (Kyslík-Acetylen)</h2>
    <div id="flame" class="flame"></div>
    <p id="desc" style="font-size:18px; font-weight:bold; margin-top:24px;">Neutrální plamen (O2:C2H2 = 1:1)</p>
    <p id="detail">Používá se pro svařování většiny ocelí. Teplota jádra cca 3100°C.</p>
    
    <div style="margin-top:24px;">
      <button onclick="setFlame('nau')">Nauhličující (Více acetylenu)</button>
      <button onclick="setFlame('neu')">Neutrální (1:1)</button>
      <button onclick="setFlame('oxi')">Oxidační (Více kyslíku)</button>
    </div>
  </div>
<script>
  function setFlame(type) {
    const f = document.getElementById('flame');
    const d = document.getElementById('desc');
    const t = document.getElementById('detail');
    if (type === 'nau') {
      f.style.background = 'linear-gradient(90deg, #ff9900 0%, #ffcc00 50%, #fff 100%)';
      f.style.transform = 'scaleX(1.2)';
      d.innerText = 'Nauhličující plamen (Přebytek acetylenu)';
      t.innerText = 'Delší zářivý závoj. Použití: litina, hliník, navařování tvrdokovů.';
    } else if (type === 'neu') {
      f.style.background = 'linear-gradient(90deg, #4facfe 0%, #00f2fe 50%, #fff 100%)';
      f.style.transform = 'scaleX(1)';
      d.innerText = 'Neutrální plamen (O2:C2H2 = 1:1)';
      t.innerText = 'Používá se pro svařování většiny ocelí. Teplota jádra cca 3100°C.';
    } else {
      f.style.background = 'linear-gradient(90deg, #0000ff 0%, #aaa 50%, #fff 100%)';
      f.style.transform = 'scaleX(0.8)';
      d.innerText = 'Oxidační plamen (Přebytek kyslíku)';
      t.innerText = 'Krátký, ostrý a syčivý plamen. Použití: mosaz, bronz (zabraňuje odpařování zinku).';
    }
  }
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "stt", "animace-svarovani.html"), "w", encoding="utf-8") as f: f.write(svar_html)

# -- SPS Animations --
prevody_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Převody | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; text-align: center; padding: 48px;}
  .gear { transform-origin: center; animation: spin infinite linear; }
  @keyframes spin { 100% { transform: rotate(360deg); } }
  .box { background: #fff; padding: 24px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  input[type=range] { width: 100%; margin: 16px 0; }
</style>
</head>
<body>
  <div class="box">
    <a href="../sps/index.html" style="color:#b0561f; text-decoration:none; font-weight:600; display:block; text-align:left;">&larr; Zpět</a>
    <h2 style="font-family:'Quicksand';color:#b0561f;">Převodový poměr</h2>
    
    <svg width="400" height="200" viewBox="0 0 400 200">
      <!-- Gear 1 (Driver) -->
      <g transform="translate(100, 100)">
        <circle r="40" fill="#5c5346" />
        <circle r="10" fill="#fbf8f3" />
        <path id="g1" class="gear" d="M-5,-45 L5,-45 L10,-40 L10,40 L5,45 L-5,45 L-10,40 L-10,-40 Z M-45,-5 L-45,5 L-40,10 L40,10 L45,5 L45,-5 L40,-10 L-40,-10 Z" fill="#b0561f" style="animation-duration: 2s;" />
      </g>
      <!-- Gear 2 (Driven) -->
      <g id="g2_container" transform="translate(190, 100)">
        <circle id="g2_base" r="40" fill="#8a8072" />
        <circle r="10" fill="#fbf8f3" />
        <path id="g2" class="gear" d="M-5,-45 L5,-45 L10,-40 L10,40 L5,45 L-5,45 L-10,40 L-10,-40 Z M-45,-5 L-45,5 L-40,10 L40,10 L45,5 L45,-5 L40,-10 L-40,-10 Z" fill="#5c5346" style="animation-duration: 2s; animation-direction: reverse;" />
      </g>
    </svg>

    <p style="font-size:18px;">Hnací kolo: <strong>n = 30 ot/min</strong></p>
    <p id="out_speed" style="font-size:18px;">Hnané kolo: <strong>n = 30 ot/min</strong></p>
    <p id="out_ratio" style="font-size:16px; color:#5c5346;">Převodový poměr i = 1</p>
    
    <label>Zvětšit/zmenšit hnané kolo (z2):</label>
    <input type="range" id="ratio" min="0.5" max="2" step="0.1" value="1" oninput="updateGear()">
  </div>
<script>
  function updateGear() {
    const val = parseFloat(document.getElementById('ratio').value);
    const g2 = document.getElementById('g2');
    const g2c = document.getElementById('g2_container');
    const g2b = document.getElementById('g2_base');
    
    // Scale gear 2
    g2.style.transform = `scale(${val})`;
    g2b.setAttribute('r', 40 * val);
    
    // Move gear 2 to mesh
    const dist = 100 + (40 * val) + 10;
    g2c.setAttribute('transform', `translate(${dist}, 100)`);
    
    // Adjust animation speed based on ratio
    const speed1 = 2; // base speed
    const speed2 = speed1 * val;
    g2.style.animationDuration = `${speed2}s`;
    
    // Update texts
    const n2 = 30 / val;
    document.getElementById('out_speed').innerHTML = `Hnané kolo: <strong>n = ${n2.toFixed(1)} ot/min</strong>`;
    document.getElementById('out_ratio').innerText = `Převodový poměr i = ${val.toFixed(2)}`;
  }
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "sps", "animace-prevodovka.html"), "w", encoding="utf-8") as f: f.write(prevody_html)

# Now link these new animations into site-structure.json so they appear automatically in the UI
import json
struct_path = os.path.join(repo_dir, "site-structure.json")
with open(struct_path, "r", encoding="utf-8") as f:
    struct = json.load(f)

# STT
if "sttCards" in struct:
    exists = any("animace-svarovani.html" in str(c.get("href")) for c in struct["sttCards"])
    if not exists:
        struct["sttCards"].insert(0, {
            "id": "doc",
            "title": "🔥 Animace: Druhy svařovacích plamenů",
            "href": "animace-svarovani.html",
            "target": "_blank",
            "status": "ready"
        })

# SPS
if "spsCards" in struct:
    exists = any("animace-prevodovka.html" in str(c.get("href")) for c in struct["spsCards"])
    if not exists:
        struct["spsCards"].insert(0, {
            "id": "doc",
            "title": "⚙️ Animace: Převodový poměr ozubených kol",
            "href": "animace-prevodovka.html",
            "target": "_blank",
            "status": "ready"
        })

with open(struct_path, "w", encoding="utf-8") as f:
    json.dump(struct, f, ensure_ascii=False, indent=2)

print("Animations created and structure updated.")
