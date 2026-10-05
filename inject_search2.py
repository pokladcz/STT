import os
import codecs

repo_dir = r"C:\Users\pokla\STT-fork"

search_js = """
<script>
  (function() {
    let searchIndex = null;
    const input = document.getElementById('searchInput');
    if (!input) return;
    
    // Create dropdown container
    const resultsContainer = document.createElement('div');
    resultsContainer.id = 'searchResults';
    resultsContainer.style.display = 'none';
    resultsContainer.style.position = 'absolute';
    resultsContainer.style.top = '100%';
    resultsContainer.style.left = '0';
    resultsContainer.style.right = '0';
    resultsContainer.style.background = '#fff';
    resultsContainer.style.border = '1px solid #ded3c2';
    resultsContainer.style.borderRadius = '12px';
    resultsContainer.style.boxShadow = '0 8px 24px rgba(35,29,22,0.15)';
    resultsContainer.style.maxHeight = '400px';
    resultsContainer.style.overflowY = 'auto';
    resultsContainer.style.zIndex = '9999';
    resultsContainer.style.marginTop = '8px';
    
    // Wrap input in a relative positioned container if not already
    const parent = input.parentElement;
    parent.style.position = 'relative';
    parent.appendChild(resultsContainer);

    input.addEventListener('focus', async () => {
      input.style.borderColor = '#b0561f';
      if (!searchIndex) {
        try {
          const inSubfolder = window.location.pathname.includes('/stt/') || 
                              window.location.pathname.includes('/sps/') || 
                              window.location.pathname.includes('/mec/') || 
                              window.location.pathname.includes('/cnc/') || 
                              window.location.pathname.includes('/mte/');
          const fetchPath = inSubfolder ? '../search-index.json' : 'search-index.json';
          
          const res = await fetch(fetchPath + '?v=' + new Date().getTime());
          searchIndex = await res.json();
        } catch (e) {
          console.error('Failed to load search index', e);
        }
      }
    });

    // Handle blur with a delay to allow clicking on links
    input.addEventListener('blur', () => {
      input.style.borderColor = '#ded3c2';
      setTimeout(() => { resultsContainer.style.display = 'none'; }, 200);
    });

    input.addEventListener('input', (e) => {
      // If there is an existing filterCards function (for large cards), call it
      if (typeof filterCards === 'function') {
         filterCards();
      }
      
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
            // score based on term frequency
            const count = (doc.content.match(new RegExp(kw, 'g')) || []).length;
            score += count;
            
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
             keywords.forEach(kw => {
                const regex = new RegExp(`(${kw})`, 'gi');
                snippet = snippet.replace(regex, '<strong style="color:#b0561f">$1</strong>');
             });
          }
          
          const inSubfolder = window.location.pathname.includes('/stt/') || 
                              window.location.pathname.includes('/sps/') || 
                              window.location.pathname.includes('/mec/') || 
                              window.location.pathname.includes('/cnc/') || 
                              window.location.pathname.includes('/mte/');
          let linkHref = r.doc.url;
          if (inSubfolder) {
             linkHref = '../' + r.doc.url;
          }
          
          return `<a href="${linkHref}" target="_blank" style="display:block;padding:12px 16px;border-bottom:1px solid #f2ece4;text-decoration:none;color:inherit;transition:background 0.2s;" onmouseover="this.style.background='#fcfaf7'" onmouseout="this.style.background='transparent'">
            <div style="font-weight:600;color:#231d16;margin-bottom:4px;font-family:'Quicksand',sans-serif;font-size:15px;">${r.doc.title} <span style="font-size:11px;color:#8a8072;background:#f2ece4;padding:2px 6px;border-radius:4px;margin-left:8px;vertical-align:middle;">${r.doc.subject}</span></div>
            ${snippet ? `<div style="font-size:13px;color:#5c5346;line-height:1.4">${snippet}</div>` : ''}
          </a>`;
        }).join('');
        resultsContainer.style.display = 'block';
      } else {
        resultsContainer.innerHTML = `<div style="padding:16px;color:#8a8072;text-align:center;font-size:14px;font-family:'IBM Plex Sans',sans-serif;">Žádné výsledky nenalezeny v PDF materiálech.</div>`;
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
    
    # If already injected, don't do it again
    if "const resultsContainer = document.createElement('div');" in html:
        print(f"Skipping {filepath} (already injected)")
        return
        
    if 'id="searchInput"' in html:
        # inject script just before </body>
        html = html.replace('</body>', search_js + '\n</body>')
        with codecs.open(filepath, "w", "utf-8") as f:
            f.write(html)
        print(f"Injected search JS into {filepath}")

# Update main index
modify_html(os.path.join(repo_dir, "index.html"))

# Also update the subject indices
for d in ['stt', 'sps', 'mec', 'cnc', 'mte']:
    idx = os.path.join(repo_dir, d, "index.html")
    modify_html(idx)

print("Done injecting search.")
