import os

repo_dir = r"C:\Users\pokla\STT-fork"
def make_dir(name): os.makedirs(os.path.join(repo_dir, name), exist_ok=True)

make_dir("3d-modely")
make_dir("vykresy")
make_dir("simulator")
make_dir("materialy")
make_dir("animace")

# --- 3D MODELY ---
viewer_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>3D Modely | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.3.0/model-viewer.min.js"></script>
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; margin: 0; padding: 48px; }
  h1 { font-family: 'Quicksand', sans-serif; color: #b0561f; font-size: 32px; }
  model-viewer { width: 100%; height: 500px; background-color: #fff; border: 1px solid #ded3c2; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); outline: none; }
  .instructions { margin-top: 16px; padding: 16px; background: #e6f7e6; color: #15561d; border-radius: 8px; font-weight: 500; }
</style>
</head>
<body>
  <a href="../index.html" style="color: #b0561f; text-decoration: none; font-weight: 600;">&larr; Zpět na rozcestník</a>
  <h1>Prohlížeč 3D Modelů</h1>
  <p style="color:#5c5346">Zkuste model otočit prstem nebo myší a přiblížit (kolečkem).</p>
  
  <model-viewer src="https://modelviewer.dev/shared-assets/models/Astronaut.glb" 
                camera-controls 
                auto-rotate 
                shadow-intensity="1">
  </model-viewer>

  <div class="instructions">
    <strong>💡 Pro vyučující:</strong> Tento blok používá technologii Google model-viewer. Jakmile budete mít své vlastní 3D modely např. ozubeného kola nebo nože ve formátu <code>.glb</code>, stačí je nahrát do složky a přepsat odkaz v atributu <code>src="..."</code>.
  </div>
</body>
</html>
"""
with open(os.path.join(repo_dir, "3d-modely", "index.html"), "w", encoding="utf-8") as f: f.write(viewer_html)

# --- VYKRESY (HOTSPOTS) ---
vykres_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interaktivní Výkresy | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; margin: 0; padding: 48px; }
  .container { position: relative; max-width: 800px; margin: 0 auto; background: #fff; border: 1px solid #ded3c2; padding: 24px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  .hotspot { position: absolute; width: 24px; height: 24px; background: #b0561f; border-radius: 50%; cursor: pointer; animation: pulse 2s infinite; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-family: sans-serif; }
  @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(176, 86, 31, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(176, 86, 31, 0); } 100% { box-shadow: 0 0 0 0 rgba(176, 86, 31, 0); } }
  #tooltip { display: none; position: absolute; background: #231d16; color: #fff; padding: 16px; border-radius: 8px; width: 250px; z-index: 10; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
</style>
</head>
<body>
  <a href="../index.html" style="color: #b0561f; text-decoration: none; font-weight: 600;">&larr; Zpět na rozcestník</a>
  <h1 style="text-align:center;font-family:'Quicksand';color:#b0561f;">Interaktivní Výkresy - Hotspots</h1>
  
  <div class="container" id="drawContainer">
    <!-- Simple Mock SVG representing a drawing -->
    <svg viewBox="0 0 400 200" width="100%" height="auto" style="border:1px dashed #ded3c2">
      <rect x="50" y="80" width="300" height="40" fill="#e5ded2" stroke="#5c5346" stroke-width="2"/>
      <rect x="100" y="60" width="200" height="80" fill="#f2ece4" stroke="#5c5346" stroke-width="2"/>
      <text x="150" y="50" font-family="sans-serif" font-size="12">Ra 1.6</text>
      <text x="250" y="160" font-family="sans-serif" font-size="12">ø50 H7/p6</text>
    </svg>

    <!-- Hotspots -->
    <div class="hotspot" style="top: 25%; left: 38%;" onclick="showTooltip('Drsnost Ra 1.6: Střední aritmetická odchylka profilu je 1.6 mikrometrů. Běžně dosahováno jemným soustružením nebo hrubým broušením.', this)">?</div>
    <div class="hotspot" style="top: 80%; left: 63%;" onclick="showTooltip('Uložení s přesahem H7/p6: Díra H7 (základní díra) a hřídel p6 (s přesahem). Používá se pro pevné spojení bez vůle.', this)">?</div>
    
    <div id="tooltip"></div>
  </div>

  <script>
    function showTooltip(text, elem) {
      const tt = document.getElementById('tooltip');
      tt.innerText = text;
      tt.style.display = 'block';
      tt.style.top = (elem.offsetTop + 30) + 'px';
      tt.style.left = elem.offsetLeft + 'px';
    }
    document.getElementById('drawContainer').addEventListener('mouseleave', () => {
      document.getElementById('tooltip').style.display = 'none';
    });
  </script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "vykresy", "index.html"), "w", encoding="utf-8") as f: f.write(vykres_html)

# --- SIMULATOR ---
sim_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Simulátor Dílny | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; margin: 0; padding: 48px; display:flex; justify-content:center; }
  .box { background: #fff; border: 1px solid #ded3c2; padding: 32px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); max-width: 600px; width: 100%; text-align: center;}
  h2 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  .btn { display: block; width: 100%; text-align: left; padding: 16px; margin: 8px 0; background: #f9f6f0; border: 1px solid #ded3c2; border-radius: 8px; cursor: pointer; transition: 0.2s; font-size:16px;}
  .btn:hover { background: #f2ece4; }
  #scenario-text { font-size: 18px; margin-bottom: 24px; color: #231d16; }
</style>
</head>
<body>
  <div class="box">
    <a href="../index.html" style="color: #8a8072; text-decoration: none; font-weight: 600; display:block; text-align:left; margin-bottom:16px;">&larr; Odejít z dílny</a>
    <h2>Situace na dílně</h2>
    <div id="scenario-text">Soustružíš ocelovou hřídel. Zjistíš, že obrobený povrch je velmi hrubý (drsný) a nůž začíná nepříjemně pískat a vibrovat. Co uděláš?</div>
    <div id="options">
      <button class="btn" onclick="act(0)">A) Zvýším posuv (f), ať to mám rychleji za sebou.</button>
      <button class="btn" onclick="act(1)">B) Snížím řeznou rychlost a přidám chladící kapalinu.</button>
      <button class="btn" onclick="act(2)">C) Zkontroluji, zda je břit nože upnutý přesně v ose rotace a zmenším posuv.</button>
      <button class="btn" onclick="act(3)">D) Nic, to je u oceli normální.</button>
    </div>
  </div>
<script>
  function act(choice) {
    const text = document.getElementById('scenario-text');
    const opts = document.getElementById('options');
    if (choice === 2) {
      text.innerHTML = "<strong>Správně!</strong> Nůž upnutý pod osou nebo nad osou drhne hřbetem nebo mění geometrii řezu, což způsobuje vibrace. Snížením posuvu navíc zlepšíš drsnost povrchu. Práce hotova!";
      opts.innerHTML = '<button class="btn" onclick="location.reload()">Hrát znovu</button>';
    } else {
      text.innerHTML = "<strong style='color:#900'>Chyba!</strong> To situaci ještě zhoršilo. Vibrace zesílily a možná jsi ulomil destičku. Zkus to znovu.";
      opts.innerHTML = '<button class="btn" onclick="location.reload()">Vrátit čas</button>';
    }
  }
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "simulator", "index.html"), "w", encoding="utf-8") as f: f.write(sim_html)

# --- MATERIAL GUIDE ---
mat_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Průvodce Materiály | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; margin: 0; padding: 48px; }
  h1 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  .filters { background: #fff; border: 1px solid #ded3c2; padding: 24px; border-radius: 12px; margin-bottom: 24px; }
  .res-card { background: #fff; border: 1px solid #ded3c2; padding: 16px; border-radius: 8px; margin-bottom: 8px; }
</style>
</head>
<body>
  <a href="../index.html" style="color: #b0561f; text-decoration: none; font-weight: 600;">&larr; Zpět na rozcestník</a>
  <h1>Průvodce výběrem materiálu</h1>
  
  <div class="filters">
    <h3>Požadavky na materiál:</h3>
    <label><input type="checkbox" id="weld" onchange="filter()"> Zaručená svařitelnost</label><br><br>
    <label><input type="checkbox" id="corr" onchange="filter()"> Odolnost proti korozi (Nerez)</label>
  </div>

  <div id="results"></div>

<script>
  const materials = [
    { name: 'S235JR', weld: true, corr: false, desc: 'Běžná konstrukční ocel, výborně svařitelná, nekorozivzdorná.' },
    { name: 'C45', weld: false, corr: false, desc: 'Ušlechtilá uhlíková ocel na hřídele. Obtížně svařitelná.' },
    { name: 'X5CrNi18-10', weld: true, corr: true, desc: 'Austenitická nerez. Výborně svařitelná, korozivzdorná.' },
    { name: 'Dural (EN AW-2024)', weld: false, corr: true, desc: 'Hliníková slitina, vysoká pevnost, špatně svařitelná.' }
  ];
  function filter() {
    const w = document.getElementById('weld').checked;
    const c = document.getElementById('corr').checked;
    const filtered = materials.filter(m => (!w || m.weld === w) && (!c || m.corr === c));
    document.getElementById('results').innerHTML = filtered.map(m => 
      `<div class="res-card"><strong>${m.name}</strong><p>${m.desc}</p></div>`
    ).join('');
  }
  filter();
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "materialy", "index.html"), "w", encoding="utf-8") as f: f.write(mat_html)

print("Created 3D Modely, Hotspots, Simulator, and Material Guide.")
