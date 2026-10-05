import os
import codecs

repo_dir = r"C:\Users\pokla\STT-fork"

kvizy_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kvízy | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../modern.css">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; color: #231d16; margin: 0; padding: 48px; }
  h1 { font-family: 'Quicksand', sans-serif; color: #b0561f; font-size: 32px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-top: 24px; }
  .card { display: block; background: #fff; border: 1px solid #ded3c2; padding: 24px; border-radius: 12px; text-decoration: none; color: inherit; }
  .icon-title { display: flex; align-items: center; gap: 12px; font-weight: 600; font-size: 20px; font-family: 'Quicksand', sans-serif; }
  .desc { color: #5c5346; margin-top: 8px; font-size: 15px; }
  .icon-emoji { font-size: 28px; }
</style>
</head>
<body>
  <a href="../index.html" style="color: #b0561f; text-decoration: none; font-weight: 600;">&larr; Zpět na rozcestník</a>
  <h1>Seznam Kvízů</h1>
  <div class="grid">
    <a href="quiz.html?subject=stt" class="card subject-card">
      <div class="icon-title"><span class="icon-emoji">🔥</span> Strojírenská Technologie (STT)</div>
      <div class="desc">Otestujte své znalosti z koroze, tváření, tepelného zpracování, odlévání a obrábění.</div>
    </a>
    <a href="quiz.html?subject=sps" class="card subject-card">
      <div class="icon-title"><span class="icon-emoji">⚙️</span> Stavba a provoz strojů (SPS)</div>
      <div class="desc">Spoje, hřídele, ložiska, převodovky a hydraulické prvky.</div>
    </a>
    <a href="quiz.html?subject=mec" class="card subject-card">
      <div class="icon-title"><span class="icon-emoji">🏗️</span> Mechanika (MEC)</div>
      <div class="desc">Statika, pružnost a pevnost, tah, tlak, smyk a ohybové momenty.</div>
    </a>
    <a href="quiz.html?subject=mte" class="card subject-card">
      <div class="icon-title"><span class="icon-emoji">🌬️</span> Měřící technika a automatizace (MTE)</div>
      <div class="desc">Základy pneumatiky, hydrauliky a zapojení rozváděčů a válců.</div>
    </a>
  </div>
</body>
</html>
"""

with open(os.path.join(repo_dir, "kvizy", "index.html"), "w", encoding="utf-8") as f:
    f.write(kvizy_html)

# Let's also update the Kalkulačky UI to add the ČSN -> EN converter
kalk_html_path = os.path.join(repo_dir, "kalkulacky", "index.html")
with codecs.open(kalk_html_path, "r", "utf-8") as f:
    kalk_html = f.read()

# Add the material converter block if it's not there
mat_calc = """
    <!-- Material Converter -->
    <div class="calc-card" style="grid-column: 1 / -1;">
      <h2>Převodník a dekodér materiálů (ČSN ↔ EN)</h2>
      <div style="display:flex; gap:16px; flex-wrap:wrap;">
        <div style="flex:1; min-width:250px;">
          <label>Zadejte normu oceli (např. 11 373, 12050, 16MnCr5):</label>
          <div style="display:flex; gap:8px;">
            <input type="text" id="mat_input" placeholder="např. 14 220" onkeyup="if(event.key==='Enter') decodeMaterial()">
            <button onclick="decodeMaterial()" style="padding: 10px 16px; background:#b0561f; color:#fff; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">Dekódovat</button>
          </div>
        </div>
      </div>
      <div id="mat_res" style="display:none; margin-top:24px; padding:24px; background:#f9f6f0; border-radius:12px; border:1px solid #ded3c2;">
        <h3 id="mat_title" style="margin-top:0; color:#b0561f;"></h3>
        <p><strong>Evropská norma (EN):</strong> <span id="mat_en" style="background:#e6f7e6; color:#15561d; padding:2px 8px; border-radius:4px; font-weight:bold;"></span></p>
        <p><strong>Česká norma (ČSN):</strong> <span id="mat_csn" style="background:#e6f7e6; color:#15561d; padding:2px 8px; border-radius:4px; font-weight:bold;"></span></p>
        <div id="mat_explanation" style="margin-top:16px; padding-top:16px; border-top:1px solid #ded3c2; line-height:1.6;"></div>
      </div>
    </div>
"""
# inject right before script
if "Převodník a dekodér materiálů" not in kalk_html:
    kalk_html = kalk_html.replace('</div>\n<script>', mat_calc + '\n  </div>\n<script>')

# add logic to script
mat_script = """
  const matDB = [
    { csn: "11373", en: "S235JR", desc: "Nelegovaná konstrukční ocel obvyklé jakosti.", expl_csn: "<ul><li><b>1</b> - Ocel tvářená</li><li><b>1</b> - Třída 11 (Konstrukční nelegované oceli)</li><li><b>3</b> - Minimální pevnost v tahu (~300 MPa)</li><li><b>7</b> - Způsob výroby (uklidněná atd.)</li><li><b>3</b> - Stav materiálu (žíháno apod.)</li></ul>", expl_en: "<ul><li><b>S</b> - Structural (konstrukční ocel)</li><li><b>235</b> - Minimální mez kluzu v MPa</li><li><b>JR</b> - Zkouška rázem v ohybu (27 J při 20°C)</li></ul>" },
    { csn: "12050", en: "C45", desc: "Nelegovaná ušlechtilá ocel pro zušlechťování.", expl_csn: "<ul><li><b>1</b> - Ocel tvářená</li><li><b>2</b> - Třída 12 (Ušlechtilé uhlíkové oceli)</li><li><b>050</b> - Střední obsah uhlíku je cca 0.50 %</li></ul>", expl_en: "<ul><li><b>C</b> - Uhlíková ocel (Carbon)</li><li><b>45</b> - Střední obsah uhlíku 0.45 %</li></ul>" },
    { csn: "14220", en: "16MnCr5", desc: "Mangan-chromová cementační ocel (legovaná).", expl_csn: "<ul><li><b>1</b> - Ocel tvářená</li><li><b>4</b> - Třída 14 (Slitinové oceli - Cr, Mn)</li><li><b>220</b> - Doplňková čísla specifikující přesné složení</li></ul>", expl_en: "<ul><li><b>16</b> - Obsah uhlíku 0.16 %</li><li><b>Mn, Cr</b> - Legovací prvky (Mangan a Chrom)</li><li><b>5</b> - Obsah manganu je 5/4 = 1.25 %</li></ul>" },
    { csn: "16343", en: "34CrNiMo6", desc: "Chrom-nikl-molybdenová ocel k zušlechťování na vysokou pevnost.", expl_csn: "<ul><li><b>1</b> - Ocel tvářená</li><li><b>6</b> - Třída 16 (Slitinové oceli - Ni, W, V)</li><li><b>343</b> - Specifikace pro vysokopevnostní ocel</li></ul>", expl_en: "<ul><li><b>34</b> - Obsah uhlíku 0.34 %</li><li><b>Cr, Ni, Mo</b> - Přísady Chrom, Nikl, Molybden</li><li><b>6</b> - Obsah přísad (děleno 4 u Cr/Ni) = 1.5%</li></ul>" },
    { csn: "19312", en: "90MnCrV8", desc: "Nástrojová legovaná ocel pro práci za studena.", expl_csn: "<ul><li><b>1</b> - Ocel tvářená</li><li><b>9</b> - Třída 19 (Nástrojové oceli)</li><li><b>3</b> - Legováno Mn, Si, V</li><li><b>12</b> - Specifikace obsahu uhlíku a legur</li></ul>", expl_en: "<ul><li><b>90</b> - Obsah uhlíku 0.90 %</li><li><b>Mn, Cr, V</b> - Přísady Mangan, Chrom, Vanad</li><li><b>8</b> - Obsah přísady 8/4 = 2%</li></ul>" }
  ];

  function decodeMaterial() {
    let val = document.getElementById('mat_input').value.toUpperCase().replace(/\s+/g, '');
    let res = matDB.find(m => m.csn === val || m.en.toUpperCase().replace(/\s+/g, '') === val);
    
    const resDiv = document.getElementById('mat_res');
    if (res) {
      document.getElementById('mat_title').innerText = res.desc;
      document.getElementById('mat_csn').innerText = "1" + res.csn.substring(1,2) + " " + res.csn.substring(2);
      document.getElementById('mat_en').innerText = res.en;
      document.getElementById('mat_explanation').innerHTML = "<h4>Rozpad značení ČSN:</h4>" + res.expl_csn + "<h4>Rozpad značení EN:</h4>" + res.expl_en;
      resDiv.style.display = 'block';
    } else {
      resDiv.style.display = 'block';
      document.getElementById('mat_title').innerText = "Materiál nebyl nalezen v lokální databázi.";
      document.getElementById('mat_csn').innerText = "N/A";
      document.getElementById('mat_en').innerText = "N/A";
      document.getElementById('mat_explanation').innerHTML = "Zkuste zadat např. <b>12 050</b>, <b>C45</b>, <b>14220</b> nebo <b>16MnCr5</b>.";
    }
  }
"""
if "decodeMaterial()" not in kalk_html:
    kalk_html = kalk_html.replace('calcCNC(); calcSPS();', 'calcCNC(); calcSPS();\n' + mat_script)
    with codecs.open(kalk_html_path, "w", "utf-8") as f:
        f.write(kalk_html)

print("Kvízy UI and Calculator ČSN done.")
