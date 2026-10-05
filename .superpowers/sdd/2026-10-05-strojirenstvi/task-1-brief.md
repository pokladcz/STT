### Task 1: Update README.md

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: None
- Produces: Updated repository documentation

- [ ] **Step 1: Write the updated README.md**

```markdown
# Výukový portál Strojírenství

Tento projekt slouží jako interaktivní výukový portál pro strojírenské předměty na **Střední průmyslová škola a Vyšší odborná škola Brno, Sokolská, příspěvková organizace**. 
Portál je vytvářen pro učitele i studenty.

## Pro studenty
- **Rozcestník:** Na hlavní stránce si vyberte požadovaný předmět (STT, SPS, MEC, Robotika, CNC, MTE).
- **Zobrazení:** Pro nejlepší zážitek u interaktivních diagramů doporučujeme stisknout klávesu **F11** pro zobrazení na celou obrazovku.
- **Vyhledávání:** Využijte vyhledávací pole v horní části pro rychlé nalezení látky.

## Pro učitele
- Portál je ideální pro promítání v hodinách. Interaktivní prvky a diagramy usnadňují vysvětlování komplexních strojírenských postupů.

## Pro přispěvatele
1. Přidejte složku s novými materiály (Markdown, HTML, PDF).
2. Zaregistrujte novou sekci do `site-structure.json`.
3. Spusťte `python sync.py` pro vygenerování menu a statických stránek.
```

- [ ] **Step 2: Commit changes**

```bash
git add README.md
git commit -m "docs: aktualizace README pro SPS a VOS Brno Sokolska"
```
