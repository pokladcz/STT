import os
import json
import codecs

repo_dir = r"C:\Users\pokla\STT-fork"

# 1. Add 5 more questions to kvizy/data/stt.json
stt_json_path = os.path.join(repo_dir, "kvizy", "data", "stt.json")
if os.path.exists(stt_json_path):
    with open(stt_json_path, "r", encoding="utf-8") as f:
        stt_q = json.load(f)
    if len(stt_q) == 10:
        stt_q.extend([
            { "q": "Co znamená pojem 'Kalitelnost'?", "options": ["Schopnost oceli dosáhnout určité tvrdosti po zakalení", "Schopnost prokalení do hloubky", "Teplota tání oceli", "Zvýšení tažnosti"], "correct": 0, "explanation": "Kalitelnost udává, jakou maximální tvrdost může daná ocel po zakalení dosáhnout (závisí hlavně na obsahu uhlíku)." },
            { "q": "Proč se provádí 'popouštění' ihned po kalení?", "options": ["K odstranění vnitřního pnutí a snížení křehkosti martenzitu", "Ke zvýšení tvrdosti", "K ochraně proti korozi", "Pro snížení nákladů"], "correct": 0, "explanation": "Zakaleny stav (martenzit) je velmi tvrdý, ale křehký a plný pnutí. Popouštění pnutí uvolní a zajistí potřebnou houževnatost." },
            { "q": "Co je to 'Cementování'?", "options": ["Sycení povrchu součásti uhlíkem u nízkouhlíkatých ocelí", "Zpevňování oceli pomocí cementu", "Nanášení ochranné vrstvy chromu", "Druh svařování"], "correct": 0, "explanation": "Cementování je chemicko-tepelné zpracování, kdy se povrch nízkouhlíkové oceli nasytí uhlíkem a následně se zakalí, čímž vznikne tvrdý povrch a houževnaté jádro." },
            { "q": "Který z následujících plynů je ochranný inertní plyn při svařování TIG/WIG?", "options": ["Kyslík", "Argon", "Acetylen", "Oxid uhličitý"], "correct": 1, "explanation": "Při svařování metodou TIG (Tungsten Inert Gas) se jako ochrana lázně používá inertní plyn, nejčastěji Argon." },
            { "q": "K čemu slouží při slévání tzv. 'jádro'?", "options": ["K vytvoření dutiny v odlitku", "Je to nálitek, který doplňuje kov", "Zpevňuje vnější povrch formy", "Slouží jako chladítko"], "correct": 0, "explanation": "Jádro se vkládá do pískové formy na místa, kde má mít budoucí odlitek dutinu nebo složitý vnitřní tvar." }
        ])
        with open(stt_json_path, "w", encoding="utf-8") as f:
            json.dump(stt_q, f, ensure_ascii=False, indent=2)

# 2. STT Animations: animace-obrabeni.html
anim_obrabeni = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<title>Geometrie břitu | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; text-align: center; padding: 48px; }
  .box { background: #fff; padding: 32px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  h2 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  svg { background: #f9f6f0; border-radius: 8px; margin: 16px 0; }
  .slider-row { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 16px; }
  .label { font-weight: bold; width: 150px; text-align: right; }
  .val { width: 50px; text-align: left; }
</style>
</head>
<body>
  <div class="box">
    <a href="../stt/index.html" style="color:#b0561f; text-decoration:none; font-weight:600; display:block; text-align:left;">&larr; Zpět</a>
    <h2>Geometrie břitu (Ortogonální řezání)</h2>
    <svg width="400" height="300" viewBox="0 0 400 300">
      <!-- Obrobek -->
      <path d="M 50,150 L 200,150 L 200,200 L 50,200 Z" fill="#b0c4de" />
      <path d="M 200,150 L 200,140 L 350,140 L 350,200 L 200,200 Z" fill="#87cefa" />
      
      <!-- Nástroj (rotates based on alpha and gamma) -->
      <g id="tool" transform="translate(200, 150)">
        <!-- The tool polygon, starting from tip at 0,0 -->
        <polygon points="0,0 80,-80 120,0" fill="#ff8c00" stroke="#cd853f" stroke-width="2" id="tool-poly"/>
      </g>
      
      <!-- Roviny -->
      <line x1="200" y1="50" x2="200" y2="250" stroke="#000" stroke-dasharray="5,5" /> <!-- Základní rovina (svislá k řezné) -->
      <line x1="50" y1="150" x2="350" y2="150" stroke="#000" stroke-dasharray="5,5" /> <!-- Řezná rovina (vodorovná) -->
    </svg>

    <div class="slider-row">
      <div class="label">Úhel hřbetu (α):</div>
      <input type="range" id="alpha" min="2" max="15" value="8" oninput="updateGeom()">
      <div class="val" id="val_alpha">8°</div>
    </div>
    <div class="slider-row">
      <div class="label">Úhel břitu (β):</div>
      <input type="range" id="beta" min="40" max="85" value="70" oninput="updateGeom()">
      <div class="val" id="val_beta">70°</div>
    </div>
    <div class="slider-row">
      <div class="label">Úhel čela (γ):</div>
      <div class="val" id="val_gamma" style="width:100px; text-align:center; font-weight:bold; color:#b0561f">12°</div>
    </div>
    <p style="font-size:14px; color:#5c5346;">Součet úhlů α + β + γ = 90° (pro nástroje s kladným úhlem čela)</p>
  </div>
<script>
  function updateGeom() {
    const alpha = parseInt(document.getElementById('alpha').value);
    let beta = parseInt(document.getElementById('beta').value);
    
    if (alpha + beta > 110) { // allow some negative gamma, max total 110 for visualization limits
        beta = 110 - alpha;
        document.getElementById('beta').value = beta;
    }
    
    const gamma = 90 - (alpha + beta);
    
    document.getElementById('val_alpha').innerText = alpha + '°';
    document.getElementById('val_beta').innerText = beta + '°';
    document.getElementById('val_gamma').innerText = gamma + '°';
    
    const tool = document.getElementById('tool-poly');
    
    // Convert angles to radians for visualization coordinates
    const aRad = alpha * Math.PI / 180;
    const bRad = beta * Math.PI / 180;
    
    // Front face (hřbet) drops down and right by angle alpha from horizontal
    // Top face (čelo) goes up and right by angle gamma from vertical
    
    // To simplify SVG drawing, we just rotate and transform a static wedge, 
    // or draw custom points.
    // x1,y1 is hřbet point
    const L1 = 100;
    const x1 = L1 * Math.cos(aRad);
    const y1 = L1 * Math.sin(aRad); // positive Y is down in SVG
    
    // x2,y2 is čelo point
    const angleCelo = (alpha + beta) * Math.PI / 180;
    const L2 = 120;
    const x2 = L2 * Math.cos(angleCelo);
    const y2 = -L2 * Math.sin(angleCelo); // negative Y is up
    
    // Draw polygon from 0,0 -> x2,y2 -> (x2+something, y2) -> x1,y1
    // A simple wedge is enough:
    tool.setAttribute("points", `0,0 ${x2},${y2} ${x2+40},0 ${x1},${y1}`);
  }
  updateGeom();
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "stt", "animace-obrabeni.html"), "w", encoding="utf-8") as f: f.write(anim_obrabeni)

# 3. Kalkulacky: Add Tolerances
kalk_path = os.path.join(repo_dir, "kalkulacky", "index.html")
with codecs.open(kalk_path, "r", "utf-8") as f:
    kalk_html = f.read()

if "SPS: Převodový poměr" in kalk_html and "Tolerování" not in kalk_html:
    tol_html = """
    <!-- Tolerování -->
    <div class="calc-card">
      <h2>Tolerování: Uložení H7/p6 vs H7/f7</h2>
      <label>Vyberte typ uložení pro hřídel ø30mm</label>
      <select id="tol_sel" onchange="calcTol()" style="width:100%; padding:10px; margin-top:4px; border-radius:8px; border:1px solid #ded3c2;">
        <option value="p6">Pevné: H7 / p6</option>
        <option value="f7">Hybné: H7 / f7</option>
      </select>
      <div id="tol_res" style="margin-top:16px;"></div>
      <div class="result" id="tol_type"></div>
    </div>
    <script>
      function calcTol() {
        const sel = document.getElementById('tol_sel').value;
        const res = document.getElementById('tol_res');
        const type = document.getElementById('tol_type');
        // Simplified hardcoded values for basic ø30-50 range
        // Dira H7 = 0 to +25 um
        // Hridel p6 = +26 to +42 um
        // Hridel f7 = -20 to -45 um
        if (sel === 'p6') {
          res.innerHTML = `Díra H7: <b>0 až +25 µm</b><br>Hřídel p6: <b>+26 až +42 µm</b>`;
          type.innerText = `Přesah: 1 až 42 µm (Uložení s přesahem)`;
          type.style.color = '#900'; type.style.background = '#ffdada';
        } else {
          res.innerHTML = `Díra H7: <b>0 až +25 µm</b><br>Hřídel f7: <b>-20 až -45 µm</b>`;
          type.innerText = `Vůle: 20 až 70 µm (Uložení s vůlí)`;
          type.style.color = '#15561d'; type.style.background = '#d4f1d4';
        }
      }
      calcTol();
    </script>
    """
    kalk_html = kalk_html.replace('</div>\n<script>', tol_html + '\n  </div>\n<script>')
    with codecs.open(kalk_path, "w", "utf-8") as f: f.write(kalk_html)

# 4. Tahaky: JSON loading mechanism
tahaky_path = os.path.join(repo_dir, "tahaky", "index.html")
tahaky_js = """
<script>
  const urlParams = new URLSearchParams(window.location.search);
  const deck = urlParams.get('deck') || 'oceli';
  
  const titleEl = document.getElementById('titleText');
  if(deck === 'cnc') titleEl.innerText = "Chytré Taháky - CNC G a M Kódy";
  
  let cards = [];
  let curr = 0;
  
  fetch(`data/${deck}.json`)
    .then(r => r.json())
    .then(data => { 
       cards = data; 
       if(cards.length > 0) {
         document.getElementById('term').innerText = cards[0].term;
         document.getElementById('definition').innerText = cards[0].def;
       }
    }).catch(e => {
       document.getElementById('term').innerText = "Chyba";
       document.getElementById('definition').innerText = "Soubor nenalezen.";
    });

  const elCard = document.getElementById('flashcard');
  elCard.addEventListener('click', () => { elCard.classList.toggle('is-flipped'); });

  function nextCard() {
    elCard.classList.remove('is-flipped');
    setTimeout(() => {
      if(cards.length > 0) {
        curr = (curr + 1) % cards.length;
        document.getElementById('term').innerText = cards[curr].term;
        document.getElementById('definition').innerText = cards[curr].def;
      }
    }, 200);
  }
</script>
"""
with codecs.open(tahaky_path, "r", "utf-8") as f: t_html = f.read()
if "fetch(`data/${deck}.json`)" not in t_html:
    # replace hardcoded script
    import re
    t_html = re.sub(r'<script>.*?</script>', tahaky_js, t_html, flags=re.DOTALL)
    t_html = t_html.replace('<h1>Chytré Taháky - Značení Ocelí (EN)</h1>', '<h1 id="titleText">Chytré Taháky - Značení Ocelí (EN)</h1>')
    # add a deck switcher
    switcher = """
    <div style="margin-bottom: 24px; display:flex; gap:16px;">
      <a href="?deck=oceli" style="text-decoration:none; padding:8px 16px; background:#fff; border:1px solid #ded3c2; border-radius:8px; color:#231d16; font-weight:bold;">Značení Ocelí</a>
      <a href="?deck=cnc" style="text-decoration:none; padding:8px 16px; background:#fff; border:1px solid #ded3c2; border-radius:8px; color:#231d16; font-weight:bold;">CNC Kódy</a>
    </div>
    <div class="scene" id="cardScene">
    """
    t_html = t_html.replace('<div class="scene" id="cardScene">', switcher)
    with codecs.open(tahaky_path, "w", "utf-8") as f: f.write(t_html)

# Create the JSON files
oceli_json = """[
  { "term": "C45E", "def": "Nelegovaná ušlechtilá ocel s obsahem uhlíku 0.45%, vhodná k zušlechťování." },
  { "term": "16MnCr5", "def": "Legovaná ocel s 0.16% C, 1.25% Mn a chromem. Určena k cementování." },
  { "term": "S235JR", "def": "Nelegovaná konstrukční ocel, mez kluzu 235 MPa." },
  { "term": "X5CrNi18-10", "def": "Vysokolegovaná korozivzdorná ocel (austenitická), 18% Cr, 10% Ni." },
  { "term": "E335", "def": "Ocel pro strojní součásti s minimální mezí kluzu 335 MPa." }
]"""
cnc_json = """[
  { "term": "G00", "def": "Rychloposuv (pohyb maximální rychlostí mimo řez)." },
  { "term": "G01", "def": "Lineární interpolace (pracovní posuv po přímce)." },
  { "term": "G02", "def": "Kruhová interpolace po směru hodinových ručiček." },
  { "term": "G03", "def": "Kruhová interpolace proti směru hodinových ručiček." },
  { "term": "M03", "def": "Zapnutí otáček vřetene po směru hodinových ručiček." },
  { "term": "M08", "def": "Zapnutí chladící kapaliny." },
  { "term": "M30", "def": "Konec programu a návrat na začátek." }
]"""
with open(os.path.join(repo_dir, "tahaky", "data", "oceli.json"), "w", encoding="utf-8") as f: f.write(oceli_json)
with open(os.path.join(repo_dir, "tahaky", "data", "cnc.json"), "w", encoding="utf-8") as f: f.write(cnc_json)

# 5. SPS-MEC Animations: mec/animace-nosnik.html
nosnik_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<title>Ohybový moment nosníku | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; text-align: center; padding: 48px; }
  .box { background: #fff; padding: 32px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  h2 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  input[type=range] { width: 100%; margin: 16px 0; }
  .graph { width: 400px; height: 100px; background: #f9f6f0; margin: 16px auto; position: relative; border-bottom: 2px solid #5c5346; }
  .moment-line { position: absolute; bottom: 0; left: 0; border-bottom: 2px solid #b0561f; transform-origin: left bottom; }
</style>
</head>
<body>
  <div class="box">
    <a href="../mec/index.html" style="color:#b0561f; text-decoration:none; font-weight:600; display:block; text-align:left;">&larr; Zpět</a>
    <h2>Průběh ohybového momentu na nosníku</h2>
    
    <!-- Nosník SVG -->
    <svg width="400" height="100" viewBox="0 0 400 100" style="overflow:visible;">
      <!-- Beam -->
      <rect x="0" y="40" width="400" height="20" fill="#8a8072" />
      <!-- Podpora A (pevná) -->
      <polygon points="0,60 -10,80 10,80" fill="#5c5346" />
      <!-- Podpora B (posuvná) -->
      <polygon points="400,60 390,80 410,80" fill="#5c5346" />
      <circle cx="395" cy="85" r="5" fill="#231d16"/>
      <circle cx="405" cy="85" r="5" fill="#231d16"/>
      
      <!-- Force Vector -->
      <g id="force_vector" transform="translate(200, 0)">
        <line x1="0" y1="0" x2="0" y2="35" stroke="#900" stroke-width="4" />
        <polygon points="0,40 -5,30 5,30" fill="#900" />
        <text x="10" y="20" fill="#900" font-weight="bold" font-family="sans-serif">F = 10 kN</text>
      </g>
    </svg>

    <label style="display:block; margin-top:16px;">Posuňte sílu F po nosníku:</label>
    <input type="range" id="pos" min="0" max="400" value="200" oninput="updateBeam()">
    
    <div style="text-align:left; font-weight:bold; margin-top:24px;">Ohybový moment (M_o):</div>
    <!-- Simple Canvas for Moment Graph -->
    <canvas id="momentGraph" width="400" height="100" style="background:#fcfaf7; border-bottom:2px solid #5c5346; margin-top:8px;"></canvas>
  </div>
<script>
  function updateBeam() {
    const pos = parseInt(document.getElementById('pos').value);
    document.getElementById('force_vector').setAttribute('transform', `translate(${pos}, 0)`);
    
    // Calculate moment graph
    // Max moment occurs at the point of force. M_max = F * a * b / L
    const L = 400;
    const a = pos;
    const b = L - a;
    const M_max = (10 * a * b) / L; // simple proportional scale
    
    const canvas = document.getElementById('momentGraph');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw triangle
    ctx.beginPath();
    ctx.moveTo(0, 100);
    ctx.lineTo(a, 100 - (M_max * 0.8)); // scaling factor for display
    ctx.lineTo(400, 100);
    ctx.fillStyle = 'rgba(176, 86, 31, 0.2)';
    ctx.fill();
    ctx.strokeStyle = '#b0561f';
    ctx.lineWidth = 2;
    ctx.stroke();
  }
  updateBeam();
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "mec", "animace-nosnik.html"), "w", encoding="utf-8") as f: f.write(nosnik_html)

# Link mec animation to structure
with open(os.path.join(repo_dir, "site-structure.json"), "r", encoding="utf-8") as f: struct = json.load(f)
if "mecCards" in struct:
    exists = any("animace-nosnik.html" in str(c.get("href")) for c in struct["mecCards"])
    if not exists:
        struct["mecCards"].insert(0, {
            "id": "doc",
            "title": "🌉 Animace: Ohybový moment nosníku",
            "href": "animace-nosnik.html",
            "target": "_blank",
            "status": "ready"
        })
with open(os.path.join(repo_dir, "site-structure.json"), "w", encoding="utf-8") as f: json.dump(struct, f, ensure_ascii=False, indent=2)


# 6. UI: Modernize globally
modern_css = """
/* Modern UI enhancements */
* { box-sizing: border-box; }
a.subject-card, .site-nav-toggle, button, input { transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1) !important; }
.site-nav-toggle { backdrop-filter: blur(12px) !important; background: rgba(255,255,255,0.85) !important; }
[data-theme='dark'] .site-nav-toggle { background: rgba(30,30,30,0.85) !important; }
a.subject-card:hover { transform: translateY(-4px) !important; box-shadow: 0 12px 24px rgba(35,29,22,0.12) !important; }
::selection { background: #b0561f; color: #fff; }
"""
with open(os.path.join(repo_dir, "modern.css"), "w", encoding="utf-8") as f: f.write(modern_css)

# Inject into index.html
with codecs.open(os.path.join(repo_dir, "index.html"), "r", "utf-8") as f: html = f.read()
if "modern.css" not in html:
    html = html.replace('</head>', '  <link rel="stylesheet" href="modern.css">\n</head>')
    with codecs.open(os.path.join(repo_dir, "index.html"), "w", "utf-8") as f: f.write(html)

for d in ['stt', 'sps', 'mec', 'cnc', 'mte']:
    p = os.path.join(repo_dir, d, "index.html")
    if os.path.exists(p):
        with codecs.open(p, "r", "utf-8") as f: sh = f.read()
        if "modern.css" not in sh:
            sh = sh.replace('</head>', '  <link rel="stylesheet" href="../modern.css">\n</head>')
            with codecs.open(p, "w", "utf-8") as f: f.write(sh)

print("All missing pieces fully implemented.")
