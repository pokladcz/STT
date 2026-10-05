import os
import codecs

repo_dir = r"C:\Users\pokla\STT-fork"

search_html = """
    <div style="font-family:'IBM Plex Sans',sans-serif;font-size:16px;font-weight:500;color:#5c5346;margin-top:8px;">SPŠ a VOŠ Brno, Sokolská</div>
    
    <div style="margin-top:24px;position:relative;max-width:600px;">
      <input type="text" id="searchInput" placeholder="Hledat materiály..." autocomplete="off" style="width:100%;box-sizing:border-box;padding:14px 20px;font-family:'IBM Plex Sans',sans-serif;font-size:16px;color:#231d16;background:#fff;border:1px solid #ded3c2;border-radius:12px;outline:none;box-shadow:0 1px 3px rgba(35,29,22,0.05);transition:border-color 0.2s">
      <div id="searchResults" style="display:none;position:absolute;top:calc(100% + 8px);left:0;right:0;background:#fff;border:1px solid #ded3c2;border-radius:12px;box-shadow:0 4px 16px rgba(35,29,22,0.1);max-height:400px;overflow-y:auto;z-index:9999;"></div>
    </div>
"""

search_js = """
<script>
  (function() {
    let searchIndex = null;
    const input = document.getElementById('searchInput');
    const resultsContainer = document.getElementById('searchResults');
    
    if (!input) return;

    input.addEventListener('focus', async () => {
      input.style.borderColor = '#b0561f';
      if (!searchIndex) {
        try {
          // Adjust path if we are in a subfolder
          const prefix = window.location.pathname.includes('/') && !window.location.pathname.endsWith('/index.html') && window.location.pathname.split('/').pop().length > 0 && !window.location.pathname.endsWith('/') && document.querySelector('title').innerText.indexOf('Rozcestník')===-1 ? '../' : (document.querySelector('title').innerText.indexOf('Rozcestník')===-1 ? '../' : './');
          
          let fetchPath = 'search-index.json';
          if (window.location.pathname.includes('/stt/') || window.location.pathname.includes('/sps/') || window.location.pathname.includes('/mec/') || window.location.pathname.includes('/cnc/') || window.location.pathname.includes('/mte/')) {
             fetchPath = '../search-index.json';
          }
          
          const res = await fetch(fetchPath + '?v=' + new Date().getTime());
          searchIndex = await res.json();
        } catch (e) {
          console.error('Failed to load search index', e);
        }
      }
    });

    input.addEventListener('blur', () => {
      input.style.borderColor = '#ded3c2';
      setTimeout(() => { resultsContainer.style.display = 'none'; }, 200);
    });

    input.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      if (!query || !searchIndex) {
        resultsContainer.style.display = 'none';
        return;
      }
      
      const keywords = query.split(' ').filter(k => k.length > 0);
      
      const results = searchIndex.map(doc => {
        let score = 0;
        let matchIndex = -1;
        const lowerTitle = doc.title.toLowerCase();
        
        keywords.forEach(kw => {
          if (lowerTitle.includes(kw)) score += 100;
          const contentMatch = doc.content.indexOf(kw);
          if (contentMatch !== -1) {
            score += 10;
            if (matchIndex === -1) matchIndex = contentMatch;
          }
        });
        
        return { doc, score, matchIndex };
      }).filter(r => r.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 15);

      if (results.length > 0) {
        resultsContainer.innerHTML = results.map(r => {
          let snippet = '';
          if (r.matchIndex !== -1) {
             const start = Math.max(0, r.matchIndex - 40);
             const end = Math.min(r.doc.content.length, r.matchIndex + 80);
             snippet = '...' + r.doc.content.substring(start, end) + '...';
             // Highlight keyword
             keywords.forEach(kw => {
                const regex = new RegExp(`(${kw})`, 'gi');
                snippet = snippet.replace(regex, '<strong>$1</strong>');
             });
          }
          
          // Determine the correct link path based on current location
          let linkHref = r.doc.url;
          if (window.location.pathname.includes('/stt/') || window.location.pathname.includes('/sps/') || window.location.pathname.includes('/mec/') || window.location.pathname.includes('/cnc/') || window.location.pathname.includes('/mte/')) {
             linkHref = '../' + r.doc.url;
          }
          
          return `<a href="${linkHref}" target="_blank" style="display:block;padding:12px 16px;border-bottom:1px solid #f2ece4;text-decoration:none;color:inherit;">
            <div style="font-weight:600;color:#b0561f;margin-bottom:4px;font-family:'Quicksand',sans-serif;">${r.doc.title} <span style="font-size:12px;color:#8a8072;background:#f2ece4;padding:2px 6px;border-radius:4px;margin-left:8px">${r.doc.subject}</span></div>
            ${snippet ? `<div style="font-size:13px;color:#5c5346;line-height:1.4">${snippet}</div>` : ''}
          </a>`;
        }).join('');
        resultsContainer.style.display = 'block';
      } else {
        resultsContainer.innerHTML = `<div style="padding:16px;color:#8a8072;text-align:center;">Žádné výsledky nenalezeny.</div>`;
        resultsContainer.style.display = 'block';
      }
    });
  })();
</script>
"""

def modify_html(filepath):
    if not os.path.exists(filepath): return
    with codecs.open(filepath, "r", "utf-8") as f:
        html = f.read()
    
    # Check if already has search
    if 'id="searchInput"' in html:
        return
        
    # Find the H1
    h1_end = html.find('</h1>')
    if h1_end == -1: return
    
    # We want to insert the subtitle and search bar after the H1
    # But wait, there is an <a> tag for "O projektu" on the same line sometimes.
    # Let's just insert it right after the closing </div> of the title row, or right after </h1> if we can't find a wrapper.
    # The home page has:
    # <div style="display:flex;align-items:baseline;justify-content:space-between;gap:24px;flex-wrap:wrap;margin:0 0 8px">
    #   <h1>...</h1>
    #   <a>...</a>
    # </div>
    
    # Let's do a reliable replacement on the main index.html
    if "Rozcestník" in html or "index.html" in filepath.lower():
        # Inject the subtitle right after the </h1> tag
        html = html.replace('</h1>', '</h1>\n' + search_html)
        
        # Inject JS before </body>
        html = html.replace('</body>', search_js + '\n</body>')
    
        with codecs.open(filepath, "w", "utf-8") as f:
            f.write(html)
        print(f"Updated {filepath}")

# Update main index
modify_html(os.path.join(repo_dir, "index.html"))

# Also update the subject indices
for d in ['stt', 'sps', 'mec', 'cnc', 'mte']:
    idx = os.path.join(repo_dir, d, "index.html")
    modify_html(idx)

print("Done injecting search.")
