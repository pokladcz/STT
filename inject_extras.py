import os
import codecs

repo_dir = r"C:\Users\pokla\STT-fork"

# 1. Update index.html links to include the new apps
with codecs.open(os.path.join(repo_dir, "index.html"), "r", "utf-8") as f:
    idx_html = f.read()

# We need to add Simulator, Materialy, 3D Modely, Hotspots to the tools section we created earlier
if "3d-modely/index.html" not in idx_html:
    old_tools = '<a href="tahaky/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">📝 Chytré Taháky</a>'
    new_tools = old_tools + """
      <a href="3d-modely/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">🧊 3D Modely</a>
      <a href="vykresy/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">📐 Interaktivní Výkresy</a>
      <a href="simulator/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">🎮 Simulátor Dílny</a>
      <a href="materialy/index.html" style="padding: 12px 24px; background: #fbf8f3; border: 1px solid #ded3c2; border-radius: 8px; font-weight: 600; text-decoration: none; color: #231d16;">⚙️ Průvodce Materiály</a>
"""
    idx_html = idx_html.replace(old_tools, new_tools)
    
# 2. Inject Gamification (Progress) & Dark Mode via script
gamification_js = """
<script>
  // GAMIFICATION & DARK MODE
  (function() {
    // DARK MODE
    const isDark = localStorage.getItem('theme') === 'dark';
    if(isDark) document.body.style.filter = 'invert(1) hue-rotate(180deg)';
    
    const themeBtn = document.createElement('button');
    themeBtn.innerText = isDark ? '☀️ Světlý režim' : '🌙 Tmavý režim';
    themeBtn.style.position = 'fixed';
    themeBtn.style.bottom = '24px';
    themeBtn.style.right = '24px';
    themeBtn.style.padding = '12px 16px';
    themeBtn.style.borderRadius = '24px';
    themeBtn.style.border = '1px solid #ded3c2';
    themeBtn.style.background = '#fff';
    themeBtn.style.cursor = 'pointer';
    themeBtn.style.zIndex = '9999';
    themeBtn.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
    themeBtn.onclick = () => {
      if(localStorage.getItem('theme') === 'dark') {
        localStorage.setItem('theme', 'light');
        location.reload();
      } else {
        localStorage.setItem('theme', 'dark');
        location.reload();
      }
    };
    document.body.appendChild(themeBtn);

    // GAMIFICATION (Green Checkmarks)
    let visited = JSON.parse(localStorage.getItem('visited_links') || '[]');
    const allLinks = document.querySelectorAll('a[target="_blank"]');
    let total = allLinks.length;
    let done = 0;

    allLinks.forEach(a => {
      const href = a.getAttribute('href');
      if (visited.includes(href)) {
        a.innerHTML += ' <span style="color:#15561d; font-weight:bold;">✓</span>';
        done++;
      }
      a.addEventListener('click', () => {
        if (!visited.includes(href)) {
          visited.push(href);
          localStorage.setItem('visited_links', JSON.stringify(visited));
          // Refresh checkmark on next load
        }
      });
    });

    // Show progress if there are links on page
    if (total > 0) {
      const prog = document.createElement('div');
      prog.innerHTML = `Postup udržitelných znalostí: <strong>${Math.round((done/total)*100)}%</strong>`;
      prog.style.position = 'absolute';
      prog.style.top = '24px';
      prog.style.left = '50%';
      prog.style.transform = 'translateX(-50%)';
      prog.style.background = '#d4f1d4';
      prog.style.color = '#15561d';
      prog.style.padding = '8px 16px';
      prog.style.borderRadius = '16px';
      prog.style.fontWeight = '500';
      prog.style.fontFamily = 'IBM Plex Sans, sans-serif';
      document.body.appendChild(prog);
    }
  })();
</script>
"""

# inject into index.html
if "GAMIFICATION" not in idx_html:
    idx_html = idx_html.replace('</body>', gamification_js + '\n</body>')

with codecs.open(os.path.join(repo_dir, "index.html"), "w", "utf-8") as f:
    f.write(idx_html)

# Also inject into the subject index.html files so gamification works there
for d in ['stt', 'sps', 'mec', 'cnc', 'mte']:
    subj_path = os.path.join(repo_dir, d, "index.html")
    if os.path.exists(subj_path):
        with codecs.open(subj_path, "r", "utf-8") as f:
            subj_html = f.read()
        if "GAMIFICATION" not in subj_html:
            subj_html = subj_html.replace('</body>', gamification_js + '\n</body>')
            with codecs.open(subj_path, "w", "utf-8") as f:
                f.write(subj_html)

print("Links, Dark Mode, and Gamification applied.")
