import os

repo_dir = r"C:\Users\pokla\STT-fork"

manifest = """{
  "name": "Výukový portál Strojírenství",
  "short_name": "Strojírenství",
  "start_url": "index.html",
  "display": "standalone",
  "background_color": "#fbf8f3",
  "theme_color": "#b0561f",
  "icons": [
    {
      "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' rx='6' fill='%23b0561f'/%3E%3Ctext x='12' y='17' font-family='Georgia,serif' font-size='12' font-weight='700' fill='%23fbf8f3' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E",
      "sizes": "192x192",
      "type": "image/svg+xml"
    }
  ]
}"""
with open(os.path.join(repo_dir, "manifest.json"), "w", encoding="utf-8") as f: f.write(manifest)

sw = """const CACHE_NAME = 'strojirenstvi-v1';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll([
        './index.html',
        './support.js',
        './site-structure.json',
        './search-index.json'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
"""
with open(os.path.join(repo_dir, "sw.js"), "w", encoding="utf-8") as f: f.write(sw)

sw_setup = """
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('./sw.js').then(reg => {
        console.log('SW registered: ', reg.scope);
      }).catch(err => {
        console.log('SW registration failed: ', err);
      });
    });
  }
</script>
"""
import codecs
idx_path = os.path.join(repo_dir, "index.html")
with codecs.open(idx_path, "r", "utf-8") as f:
    html = f.read()
if "serviceWorker" not in html:
    html = html.replace('</head>', '  <link rel="manifest" href="manifest.json">\n</head>')
    html = html.replace('</body>', sw_setup + '\n</body>')
    with codecs.open(idx_path, "w", "utf-8") as f:
        f.write(html)
print("PWA files created and injected.")
