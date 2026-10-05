import os
import json

repo_dir = r"C:\Users\pokla\STT-fork"

# 1. CNC Toolpath Animation
cnc_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CNC Interpolace | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; text-align: center; padding: 48px; }
  .box { background: #fff; padding: 32px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  h2 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  canvas { background: #f9f6f0; border: 1px solid #ded3c2; border-radius: 8px; margin: 16px 0; }
  button { padding: 10px 20px; font-size: 16px; font-weight: bold; border-radius: 8px; border: 1px solid #ded3c2; background: #fff; cursor: pointer; transition: 0.2s; }
  button:hover { background: #e5ded2; }
  #desc { font-weight: 600; color: #15561d; height: 30px; font-size: 18px; }
</style>
</head>
<body>
  <div class="box">
    <a href="../cnc/index.html" style="color:#b0561f; text-decoration:none; font-weight:600; display:block; text-align:left;">&larr; Zpět na CNC</a>
    <h2>CNC Interpolace dráhy nástroje</h2>
    <canvas id="c" width="500" height="300"></canvas>
    <div id="desc">Vyberte kód z nabídky:</div>
    <div style="margin-top: 16px; display:flex; gap:8px; justify-content:center;">
      <button onclick="runG00()">G00</button>
      <button onclick="runG01()">G01</button>
      <button onclick="runG02()">G02</button>
      <button onclick="runG03()">G03</button>
    </div>
  </div>
<script>
  const canvas = document.getElementById('c');
  const ctx = canvas.getContext('2d');
  let toolX = 50, toolY = 250;
  let animating = false;

  function drawGrid() {
    ctx.clearRect(0,0,500,300);
    ctx.strokeStyle = '#e5ded2';
    for(let i=0; i<500; i+=50) {
      ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,300); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(500,i); ctx.stroke();
    }
    // raw block
    ctx.fillStyle = '#b0c4de';
    ctx.fillRect(150, 100, 200, 150);
  }

  function drawTool(x, y) {
    ctx.beginPath();
    ctx.arc(x, y, 6, 0, Math.PI*2);
    ctx.fillStyle = 'red';
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.stroke();
  }

  function animatePath(points, timeMs, color, text) {
    if(animating) return;
    animating = true;
    document.getElementById('desc').innerHTML = text;
    let start = performance.now();
    
    function frame(t) {
      let progress = (t - start) / timeMs;
      if (progress > 1) progress = 1;
      
      drawGrid();
      
      // Draw path so far
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      let curIdx = Math.floor(progress * (points.length-1));
      for(let i=1; i<=curIdx; i++) {
        ctx.lineTo(points[i].x, points[i].y);
      }
      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      if (color === 'red') ctx.setLineDash([5, 5]); else ctx.setLineDash([]);
      ctx.stroke();
      ctx.setLineDash([]);
      
      toolX = points[curIdx].x;
      toolY = points[curIdx].y;
      drawTool(toolX, toolY);
      
      if (progress < 1) requestAnimationFrame(frame);
      else animating = false;
    }
    requestAnimationFrame(frame);
  }

  function runG00() {
    let pts = [];
    for(let i=0; i<=20; i++) pts.push({x: 50 + (100)*i/20, y: 250 - (150)*i/20});
    animatePath(pts, 500, 'red', '<span style="color:red">G00 - Rychloposuv:</span> Pohyb mimo materiál maximální rychlostí stroje.');
  }
  function runG01() {
    let pts = [];
    for(let i=0; i<=100; i++) pts.push({x: 150 + (200)*i/100, y: 100});
    animatePath(pts, 2000, 'green', '<span style="color:green">G01 - Lineární interpolace:</span> Pracovní posuv po přímce (např. soustružení válce).');
  }
  function runG02() {
    let pts = [];
    for(let i=0; i<=100; i++) {
      let a = Math.PI - (Math.PI/2)*i/100; // 180 to 90 deg
      pts.push({x: 250 + 100*Math.cos(a), y: 200 - 100*Math.sin(a)});
    }
    animatePath(pts, 2000, 'blue', '<span style="color:blue">G02 - Kruhová interpolace CW:</span> Pracovní posuv po oblouku po směru hodin.');
  }
  function runG03() {
    let pts = [];
    for(let i=0; i<=100; i++) {
      let a = Math.PI*1.5 + (Math.PI/2)*i/100; // 270 to 360
      pts.push({x: 150 + 100*Math.cos(a), y: 200 + 100*Math.sin(a)}); // adjusted just for visuals
    }
    animatePath(pts, 2000, '#b0561f', '<span style="color:#b0561f">G03 - Kruhová interpolace CCW:</span> Pracovní posuv po oblouku proti směru hodin.');
  }
  
  drawGrid(); drawTool(50,250);
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "cnc", "animace-drahy.html"), "w", encoding="utf-8") as f: f.write(cnc_html)

# 2. MTE Cylinder Animation
mte_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pneumatický válec | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; text-align: center; padding: 48px; }
  .box { background: #fff; padding: 32px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  h2 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  button { padding: 10px 20px; font-size: 16px; font-weight: bold; border-radius: 8px; border: 1px solid #ded3c2; background: #fff; cursor: pointer; transition: 0.2s; margin: 0 8px; }
  button:hover { background: #e5ded2; }
</style>
</head>
<body>
  <div class="box">
    <a href="../mte/index.html" style="color:#b0561f; text-decoration:none; font-weight:600; display:block; text-align:left;">&larr; Zpět na MTE</a>
    <h2>Dvojčinný pneumatický válec</h2>
    
    <svg width="500" height="200" viewBox="0 0 500 200">
      <!-- Válec -->
      <rect x="50" y="50" width="200" height="100" fill="#e5ded2" stroke="#5c5346" stroke-width="4" />
      
      <!-- Pístnice a píst -->
      <g id="piston" style="transition: transform 1s ease-in-out;">
        <rect x="60" y="60" width="20" height="80" fill="#231d16" /> <!-- píst -->
        <rect x="80" y="90" width="300" height="20" fill="#8a8072" /> <!-- tyč -->
      </g>
      
      <!-- Otvory pro vzduch -->
      <circle cx="70" cy="40" r="10" fill="#4facfe" id="air-left" style="opacity:0" />
      <circle cx="230" cy="40" r="10" fill="#4facfe" id="air-right" style="opacity:1" />
      <text x="65" y="30" font-family="sans-serif">A</text>
      <text x="225" y="30" font-family="sans-serif">B</text>
    </svg>

    <div style="margin-top:24px;">
      <button onclick="extend()">Tlak do portu A (Vysunout)</button>
      <button onclick="retract()">Tlak do portu B (Zasunout)</button>
    </div>
  </div>
<script>
  function extend() {
    document.getElementById('piston').style.transform = 'translateX(160px)';
    document.getElementById('air-left').style.opacity = '1';
    document.getElementById('air-right').style.opacity = '0';
  }
  function retract() {
    document.getElementById('piston').style.transform = 'translateX(0px)';
    document.getElementById('air-left').style.opacity = '0';
    document.getElementById('air-right').style.opacity = '1';
  }
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "mte", "animace-valec.html"), "w", encoding="utf-8") as f: f.write(mte_html)

# 3. STT Tahova zkouska
tah_html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tahová zkouška | Výukový portál</title>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { background: #fbf8f3; font-family: 'IBM Plex Sans', sans-serif; text-align: center; padding: 48px; }
  .box { background: #fff; padding: 32px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  h2 { font-family: 'Quicksand', sans-serif; color: #b0561f; }
  canvas { border-left: 2px solid #231d16; border-bottom: 2px solid #231d16; margin: 16px; }
  button { padding: 10px 20px; font-size: 16px; font-weight: bold; border-radius: 8px; border: 1px solid #ded3c2; background: #fff; cursor: pointer; transition: 0.2s; }
  button:hover { background: #d4f1d4; color: #15561d; border-color: #15561d;}
</style>
</head>
<body>
  <div class="box">
    <a href="../stt/index.html" style="color:#b0561f; text-decoration:none; font-weight:600; display:block; text-align:left;">&larr; Zpět na STT</a>
    <h2>Tahová zkouška (Ocel se zřetelnou mezí kluzu)</h2>
    <div style="display:flex; justify-content:center; align-items:center;">
      <canvas id="c" width="400" height="300"></canvas>
      <svg width="100" height="300">
        <rect x="30" y="20" width="40" height="20" fill="#5c5346"/>
        <rect x="30" y="260" width="40" height="20" fill="#5c5346"/>
        <!-- Sample -->
        <rect id="sample" x="40" y="40" width="20" height="220" fill="#b0c4de" stroke="#5c5346" />
      </svg>
    </div>
    <button onclick="runTest()">Spustit trhací zkoušku</button>
  </div>
<script>
  const canvas = document.getElementById('c');
  const ctx = canvas.getContext('2d');
  
  // Draw axes
  ctx.font = '14px sans-serif';
  ctx.fillText('Napětí σ [MPa]', 10, 20);
  ctx.fillText('Prodloužení ε [%]', 280, 290);
  
  // Data for mild steel curve (simplified path)
  const curve = [
    {x:0, y:0},
    {x:50, y:200}, // Pružná oblast (Hooke)
    {x:60, y:200}, {x:65, y:190}, {x:75, y:195}, // Mez kluzu Re
    {x:250, y:260}, // Mez pevnosti Rm
    {x:350, y:210}  // Bod lomu
  ];

  function runTest() {
    ctx.clearRect(0,0,400,300);
    ctx.fillText('Napětí σ [MPa]', 10, 20);
    ctx.fillText('Prodloužení ε [%]', 280, 290);
    
    let t = 0;
    const sample = document.getElementById('sample');
    
    let intr = setInterval(() => {
      t++;
      if (t > 100) { clearInterval(intr); return; }
      
      // Calculate current point on curve
      let progress = t / 100;
      let targetX = progress * 350;
      let targetY = 0;
      
      // Find segment
      for(let i=0; i<curve.length-1; i++) {
         if (targetX >= curve[i].x && targetX <= curve[i+1].x) {
             let segPct = (targetX - curve[i].x) / (curve[i+1].x - curve[i].x);
             targetY = curve[i].y + segPct * (curve[i+1].y - curve[i].y);
             break;
         }
      }
      
      // Draw graph
      ctx.beginPath();
      ctx.moveTo(0, 300);
      for(let i=0; i<curve.length; i++) {
         if(curve[i].x <= targetX) {
           ctx.lineTo(curve[i].x, 300 - curve[i].y);
         }
      }
      ctx.lineTo(targetX, 300 - targetY);
      ctx.strokeStyle = 'red';
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Animate sample visually
      // Stretch height, narrow width
      let currentHeight = 220 + (targetX / 5);
      let currentWidth = 20 - (targetX / 30);
      sample.setAttribute('height', currentHeight);
      sample.setAttribute('width', currentWidth);
      sample.setAttribute('x', 50 - (currentWidth / 2));
      
      if (t === 100) {
        ctx.fillText('LOM 💥', targetX, 300 - targetY - 10);
      }
    }, 50);
  }
</script>
</body>
</html>
"""
with open(os.path.join(repo_dir, "stt", "animace-tahovka.html"), "w", encoding="utf-8") as f: f.write(tah_html)

# Add to site structure
struct_path = os.path.join(repo_dir, "site-structure.json")
with open(struct_path, "r", encoding="utf-8") as f: struct = json.load(f)

if "cncCards" in struct and not any("animace-drahy" in str(c) for c in struct["cncCards"]):
    struct["cncCards"].insert(0, {"id": "doc", "title": "🔴 Animace: CNC Interpolace a G-kódy", "href": "animace-drahy.html", "target": "_blank", "status": "ready"})
if "mteCards" in struct and not any("animace-valec" in str(c) for c in struct["mteCards"]):
    struct["mteCards"].insert(0, {"id": "doc", "title": "🌬️ Animace: Pneumatický válec", "href": "animace-valec.html", "target": "_blank", "status": "ready"})
if "sttCards" in struct and not any("animace-tahovka" in str(c) for c in struct["sttCards"]):
    struct["sttCards"].insert(0, {"id": "doc", "title": "📈 Animace: Tahová zkouška oceli", "href": "animace-tahovka.html", "target": "_blank", "status": "ready"})

with open(struct_path, "w", encoding="utf-8") as f: json.dump(struct, f, ensure_ascii=False, indent=2)

print("Animations created and structure updated.")
