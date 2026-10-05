import os

repo_dir = r"C:\Users\pokla\STT-fork"

# Helper for creating dirs
def make_dir(name):
    os.makedirs(os.path.join(repo_dir, name), exist_ok=True)

make_dir("kvizy")
make_dir("kvizy/data")
make_dir("kalkulacky")
make_dir("tahaky")
make_dir("tahaky/data")

# --- KVIZY ---
kvizy_index = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kvízy | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; color: #231d16; margin: 0; padding: 48px; }
  h1 { font-family: 'Quicksand', sans-serif; color: #b0561f; font-size: 32px; }
  .card { display: block; background: #fff; border: 1px solid #ded3c2; padding: 24px; border-radius: 12px; margin-bottom: 16px; text-decoration: none; color: inherit; transition: box-shadow 0.2s, transform 0.2s; }
  .card:hover { box-shadow: 0 8px 24px rgba(35,29,22,0.1); transform: translateY(-2px); }
  .title { font-weight: 600; font-size: 20px; font-family: 'Quicksand', sans-serif; }
  .desc { color: #5c5346; margin-top: 8px; }
</style>
</head>
<body>
  <a href="../index.html" style="color: #b0561f; text-decoration: none; font-weight: 600;">&larr; Zpět na rozcestník</a>
  <h1>Seznam Kvízů</h1>
  <a href="quiz.html?subject=stt" class="card">
    <div class="title">Strojírenská Technologie (STT)</div>
    <div class="desc">Otestujte své znalosti z koroze, tváření, tepelného zpracování a odlévání.</div>
  </a>
</body>
</html>
"""
with open(os.path.join(repo_dir, "kvizy", "index.html"), "w", encoding="utf-8") as f: f.write(kvizy_index)

kvizy_app = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kvíz</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; color: #231d16; margin: 0; padding: 48px; display: flex; justify-content: center; }
  .container { background: #fff; border: 1px solid #ded3c2; padding: 32px; border-radius: 16px; max-width: 600px; width: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  h2 { font-family: 'Quicksand', sans-serif; color: #b0561f; margin-top: 0; }
  .option { display: block; width: 100%; text-align: left; padding: 16px; margin: 8px 0; background: #f9f6f0; border: 1px solid #ded3c2; border-radius: 8px; cursor: pointer; font-family: 'IBM Plex Sans', sans-serif; font-size: 16px; transition: all 0.2s; }
  .option:hover { background: #f2ece4; }
  .option.correct { background: #d4f1d4; border-color: #15561d; color: #15561d; }
  .option.wrong { background: #ffdada; border-color: #900; color: #900; }
  #explanation { display: none; margin-top: 16px; padding: 16px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px; }
  #nextBtn { display: none; margin-top: 24px; padding: 12px 24px; background: #b0561f; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600; }
</style>
</head>
<body>
<div class="container">
  <div id="progress" style="color: #8a8072; font-weight: 600; margin-bottom: 16px;"></div>
  <h2 id="question">Načítám kvíz...</h2>
  <div id="options"></div>
  <div id="explanation"></div>
  <button id="nextBtn">Další otázka</button>
</div>
<script>
  const urlParams = new URLSearchParams(window.location.search);
  const subject = urlParams.get('subject') || 'stt';
  
  let questions = [];
  let currentIndex = 0;
  let score = 0;

  fetch(`data/${subject}.json?v=${new Date().getTime()}`)
    .then(r => r.json())
    .then(data => { questions = data; showQuestion(); })
    .catch(e => document.getElementById('question').innerText = "Chyba při načítání kvízu.");

  function showQuestion() {
    if (currentIndex >= questions.length) {
      document.querySelector('.container').innerHTML = `<h2>Kvíz dokončen!</h2><p style="font-size:18px">Vaše skóre: <strong>${score} z ${questions.length}</strong></p><a href="index.html" style="color:#b0561f;font-weight:600;text-decoration:none;">&larr; Zpět na seznam kvízů</a>`;
      return;
    }
    const q = questions[currentIndex];
    document.getElementById('progress').innerText = `Otázka ${currentIndex + 1} z ${questions.length}`;
    document.getElementById('question').innerText = q.q;
    const opts = document.getElementById('options');
    opts.innerHTML = '';
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('nextBtn').style.display = 'none';

    q.options.forEach((opt, idx) => {
      const btn = document.createElement('button');
      btn.className = 'option';
      btn.innerText = opt;
      btn.onclick = () => selectOption(btn, idx, q);
      opts.appendChild(btn);
    });
  }

  function selectOption(btn, idx, q) {
    const opts = document.querySelectorAll('.option');
    opts.forEach(b => b.disabled = true);
    
    if (idx === q.correct) {
      btn.classList.add('correct');
      score++;
    } else {
      btn.classList.add('wrong');
      opts[q.correct].classList.add('correct');
      const expl = document.getElementById('explanation');
      expl.innerText = q.explanation;
      expl.style.display = 'block';
    }
    const nextBtn = document.getElementById('nextBtn');
    nextBtn.style.display = 'block';
    nextBtn.onclick = () => { currentIndex++; showQuestion(); };
  }
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "kvizy", "quiz.html"), "w", encoding="utf-8") as f: f.write(kvizy_app)

stt_json = """[
  { "q": "Jaký je hlavní rozdíl mezi tvářením za studena a za tepla?", "options": ["Tváření za tepla probíhá nad rekrystalizační teplotou", "Tváření za tepla je vždy přesnější", "Při tváření za studena nedochází ke zpevnění", "Neexistuje žádný rozdíl"], "correct": 0, "explanation": "Tváření za tepla probíhá nad teplotou rekrystalizace, proto při něm nedochází ke zpevnění." },
  { "q": "Který typ koroze vzniká při styku dvou různých kovů v elektrolytu?", "options": ["Štěrbinová", "Galvanická", "Rovnoměrná", "Bodová"], "correct": 1, "explanation": "Galvanická koroze vzniká spojením dvou kovů s rozdílným elektrochemickým potenciálem." },
  { "q": "Při jaké teplotě probíhá austenitizace u ocelí?", "options": ["Pod teplotou A1", "Nad teplotou Ac3 (příp. Ac1 u podeutektoidních)", "Při teplotě tání", "Při pokojové teplotě"], "correct": 1, "explanation": "Austenitizace vyžaduje ohřev do oblasti stabilního austenitu, tedy nad teplotu Ac3." },
  { "q": "Co znamená pojem 'zpevnění' u kovů?", "options": ["Zvýšení meze kluzu při plastické deformaci za studena", "Zvýšení pevnosti legováním", "Kalení do oleje", "Změkčení kovu"], "correct": 0, "explanation": "Zpevnění (deformační zpevnění) je nárůst odporu proti další plastické deformaci při tváření za studena." },
  { "q": "Jaká forma se používá pro metodu 'Lost foam' (lití na vytavitelný/odpařitelný model)?", "options": ["Kovová kokila", "Model z polystyrenu zasypaný pískem", "Keramická skořepina", "Sádrová forma"], "correct": 1, "explanation": "Metoda Lost foam využívá polystyrenový model, který se při nalití taveniny odpaří." },
  { "q": "Co je to 'Pilling-Bedworthovo pravidlo'?", "options": ["Pravidlo pro výpočet rychlosti obrábění", "Podmínka určující ochranné vlastnosti oxidové vrstvy při korozi", "Pravidlo pro výpočet slévárenského smrštění", "Týká se sváření v ochranné atmosféře"], "correct": 1, "explanation": "PB pravidlo porovnává objem vzniklého oxidu s objemem zreagovaného kovu." },
  { "q": "Jaký plyn se nejčastěji používá u metody svařování MAG (Metal Active Gas)?", "options": ["Argon", "Helium", "CO2 nebo směsný plyn s CO2", "Vodík"], "correct": 2, "explanation": "Metoda MAG používá aktivní plyn, nejčastěji CO2 nebo jeho směsi s Argonem." },
  { "q": "Který z následujících procesů patří do Práškové metalurgie?", "options": ["Slinování", "Kování v zápustce", "Hluboké tažení", "Kokilové lití"], "correct": 0, "explanation": "Základem práškové metalurgie je lisování kovových prášků a následné slinování (sintrování)." },
  { "q": "Co udává 'modul ozubení' (m)?", "options": ["Rozteč dělená pí (p/π)", "Počet zubů dělený průměrem", "Tloušťku zubu v palcích", "Úhel záběru"], "correct": 0, "explanation": "Modul je poměr rozteče a čísla pí (m = p/π) a je základním parametrem ozubených kol." },
  { "q": "Jaká je funkce nálitku u odlitků?", "options": ["Estetický prvek", "Slouží jako zásobárna tekutého kovu pro doplňování objemu při smršťování", "Odvádí plyny z formy", "Zpevňuje odlitek"], "correct": 1, "explanation": "Nálitek tuhne jako poslední a doplňuje tekutý kov do míst, která se při tuhnutí smršťují." }
]"""
with open(os.path.join(repo_dir, "kvizy", "data", "stt.json"), "w", encoding="utf-8") as f: f.write(stt_json)

# --- KALKULACKY ---
kalk_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Inženýrské kalkulačky | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; color: #231d16; margin: 0; padding: 48px; }
  h1 { font-family: 'Quicksand', sans-serif; color: #b0561f; font-size: 32px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 24px; }
  .calc-card { background: #fff; border: 1px solid #ded3c2; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  h2 { font-family: 'Quicksand', sans-serif; color: #231d16; font-size: 20px; margin-top: 0; border-bottom: 2px solid #f2ece4; padding-bottom: 8px; }
  label { display: block; font-size: 14px; font-weight: 600; color: #5c5346; margin-top: 12px; }
  input { width: 100%; box-sizing: border-box; padding: 10px; margin-top: 4px; border: 1px solid #ded3c2; border-radius: 8px; font-family: inherit; font-size: 16px; }
  .result { margin-top: 16px; padding: 12px; background: #e6f7e6; border-radius: 8px; font-weight: 600; color: #15561d; }
</style>
</head>
<body>
  <a href="../index.html" style="color: #b0561f; text-decoration: none; font-weight: 600;">&larr; Zpět na rozcestník</a>
  <h1>Inženýrské kalkulačky</h1>
  <div class="grid">
    <!-- CNC -->
    <div class="calc-card">
      <h2>CNC: Řezná rychlost a otáčky</h2>
      <label>Průměr (d) [mm]</label>
      <input type="number" id="cnc_d" value="50" oninput="calcCNC()">
      <label>Řezná rychlost (vc) [m/min]</label>
      <input type="number" id="cnc_vc" value="100" oninput="calcCNC_from_vc()">
      <div class="result" id="cnc_res">Otáčky (n): 636.6 ot/min</div>
    </div>
    <!-- SPS -->
    <div class="calc-card">
      <h2>SPS: Převodový poměr (i)</h2>
      <label>Hnací kolo zuby (z1)</label>
      <input type="number" id="sps_z1" value="20" oninput="calcSPS()">
      <label>Hnané kolo zuby (z2)</label>
      <input type="number" id="sps_z2" value="60" oninput="calcSPS()">
      <div class="result" id="sps_res">Převodový poměr (i): 3</div>
    </div>
  </div>
<script>
  function calcCNC() {
    const d = parseFloat(document.getElementById('cnc_d').value);
    const vc = parseFloat(document.getElementById('cnc_vc').value);
    if(d && vc) {
      const n = (vc * 1000) / (Math.PI * d);
      document.getElementById('cnc_res').innerText = `Otáčky (n): ${n.toFixed(1)} ot/min`;
    }
  }
  function calcCNC_from_vc() { calcCNC(); }
  function calcSPS() {
    const z1 = parseFloat(document.getElementById('sps_z1').value);
    const z2 = parseFloat(document.getElementById('sps_z2').value);
    if(z1 && z2) document.getElementById('sps_res').innerText = `Převodový poměr (i): ${(z2/z1).toFixed(2)}\n(Převod do pomala/rychla)`;
  }
  calcCNC(); calcSPS();
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "kalkulacky", "index.html"), "w", encoding="utf-8") as f: f.write(kalk_html)

# --- TAHAKY ---
tahaky_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Taháky (Flashcards) | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
  h1 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  .scene { width: 350px; height: 220px; perspective: 1000px; cursor: pointer; margin-bottom: 24px; }
  .card { width: 100%; height: 100%; position: relative; transition: transform 0.6s; transform-style: preserve-3d; }
  .card.is-flipped { transform: rotateY(180deg); }
  .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; border: 1px solid #ded3c2; border-radius: 16px; box-shadow: 0 8px 24px rgba(35,29,22,0.1); padding: 24px; box-sizing: border-box; text-align: center; }
  .card-face.back { transform: rotateY(180deg); background: #fcfaf7; }
  .term { font-size: 32px; font-weight: 700; font-family: 'Quicksand', sans-serif; color: #231d16; }
  .def { font-size: 18px; color: #5c5346; }
  .controls { display: flex; gap: 16px; }
  button { padding: 12px 24px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; border: none; font-family: inherit; }
  .btn-know { background: #d4f1d4; color: #15561d; }
  .btn-dont { background: #ffdada; color: #900; }
</style>
</head>
<body>
  <a href="../index.html" style="position:absolute; top:24px; left:24px; color: #b0561f; text-decoration: none; font-weight: 600;">&larr; Zpět na rozcestník</a>
  <h1>Chytré Taháky - Značení Ocelí (EN)</h1>
  
  <div class="scene" id="cardScene">
    <div class="card" id="flashcard">
      <div class="card-face front">
        <div class="term" id="term">C45E</div>
      </div>
      <div class="card-face back">
        <div class="def" id="definition">Nelegovaná ušlechtilá ocel s obsahem uhlíku 0.45%.</div>
      </div>
    </div>
  </div>

  <div class="controls">
    <button class="btn-dont" onclick="nextCard()">Nevěděl jsem</button>
    <button class="btn-know" onclick="nextCard()">Věděl jsem</button>
  </div>

<script>
  const cards = [
    { term: 'C45E', def: 'Nelegovaná ušlechtilá ocel s obsahem uhlíku 0.45%, vhodná k zušlechťování.' },
    { term: '16MnCr5', def: 'Legovaná ocel s 0.16% C, 1.25% Mn (5/4) a chromem. Určena k cementování.' },
    { term: 'S235JR', def: 'Nelegovaná konstrukční ocel, mez kluzu 235 MPa, vrubová houževnatost při 20°C.' },
    { term: 'X5CrNi18-10', def: 'Vysokolegovaná korozivzdorná ocel (austenitická), 0.05% C, 18% Cr, 10% Ni.' },
    { term: 'E335', def: 'Ocel pro strojní součásti s minimální mezí kluzu 335 MPa.' }
  ];
  let curr = 0;
  
  const elCard = document.getElementById('flashcard');
  elCard.addEventListener('click', () => { elCard.classList.toggle('is-flipped'); });

  function nextCard() {
    elCard.classList.remove('is-flipped');
    setTimeout(() => {
      curr = (curr + 1) % cards.length;
      document.getElementById('term').innerText = cards[curr].term;
      document.getElementById('definition').innerText = cards[curr].def;
    }, 200); // wait for flip back animation
  }
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "tahaky", "index.html"), "w", encoding="utf-8") as f: f.write(tahaky_html)

# Add links to index.html
with open(os.path.join(repo_dir, "index.html"), "r", encoding="utf-8") as f:
    idx_html = f.read()

# Add a section under cardsContainer
links_html = """
  <div style="max-width:1080px; margin: 48px auto; background: #fff; border: 1px solid #ded3c2; padding: 24px; border-radius: 16px;">
    <h2 style="font-family:'Quicksand',sans-serif; color:#b0561f; margin-top:0;">Nové interaktivní nástroje</h2>
    <div style="display: flex; gap: 16px; flex-wrap: wrap;">
      <a href="kvizy/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">🧠 Kvízy</a>
      <a href="kalkulacky/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">🧮 Kalkulačky</a>
      <a href="tahaky/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">📝 Chytré Taháky</a>
    </div>
  </div>
"""

if "Nové interaktivní nástroje" not in idx_html:
    idx_html = idx_html.replace('</x-dc>', links_html + '\n</x-dc>')
    with open(os.path.join(repo_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx_html)
