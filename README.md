# ⚙️ Výukový portál Strojírenství

Tento projekt je interaktivní výukový portál pro strojírenské předměty, vytvořený na míru pro studenty a učitele **Střední průmyslové školy a Vyšší odborné školy Brno, Sokolská, příspěvková organizace**.

Portál sjednocuje výukové materiály z různých oborů do jednoho moderního rozhraní s interaktivními diagramy, animacemi a rychlým vyhledáváním.

---

## 📚 Obsah portálu
Na jedné úvodní obrazovce (rozcestníku) naleznete všechny dostupné materiály:
* **Strojírenská technologie (STT):** Plně interaktivní kapitoly s animacemi (Vnitřní stavba kovů, Koroze, Tváření, Prášková metalurgie, Značení ocelí, Odlévání).
* **Další odborné předměty:** Přehledné rozcestníky k dokumentům a materiálům pro **SPS** (Stavba a provoz strojů), **MEC** (Mechanika), **CNC** (Programování) a **MTE** (Měření a testování).

---

## 🌟 Hlavní funkce
* 📱 **Plně responzivní:** Web se automaticky přizpůsobí (přeskládá dlaždice) pro **počítače, tablety i mobilní telefony**.
* 🔍 **Rychlé vyhledávání:** Okamžité fulltextové filtrování dlaždic přímo na hlavní stránce.
* 🖱️ **Interaktivní diagramy:** Krok-za-krokem animované technické postupy ideální k pochopení složité látky.

---

## 🚀 Jak stránku otevřít a používat

### 1. Online přístup (Kdekoliv a z jakéhokoliv zařízení)
Portál je nasazen na GitHub Pages. Stačí otevřít tento odkaz v jakémkoliv prohlížeči (na PC, mobilu či tabletu):
👉 **[Zobrazit Výukový portál](https://pokladcz.github.io/STT/)**

### 2. Spuštění lokálně na počítači (Offline)
Projekt využívá moderní JavaScript (asynchronní načítání ze souboru `site-structure.json`). Z bezpečnostních důvodů prohlížeče (CORS policy) *nebude fungovat*, pokud na soubor `index.html` pouze dvakrát kliknete. Musíte využít lokální server:

* **Možnost A - Pomocí Pythonu (Doporučeno):**
  Otevřete si terminál (Příkazový řádek / PowerShell) ve složce s tímto projektem a napište:
  ```bash
  python -m http.server 8000
  ```
  Následně jděte na: `http://localhost:8000`

* **Možnost B - Pomocí VS Code (Live Server):**
  Nainstalujte si rozšíření **Live Server**, klikněte pravým tlačítkem na `index.html` a zvolte **"Open with Live Server"**.

---

## 👨‍🎓 Pro studenty
* **Plná obrazovka:** Pro nejlepší zážitek u interaktivních schémat a animací (zejména u STT a CNC) doporučujeme na počítači stisknout klávesu **F11**.
* **Vyhledávání:** Využijte vyhledávací pole v horní části hlavní stránky pro rychlé nalezení tématu.

## 👨‍🏫 Pro učitele
Tento portál je navržen jako ideální nástroj pro **promítání na projektoru v hodinách**.
* Neobsahuje rušivé elementy, na obrazovce je jen probíraná látka.
* Interaktivní fáze diagramů (např. u slitin nebo koroze) lze krokovat dopředu i dozadu, což pomáhá udržet pozornost žáků.

---

## 🛠️ Pro autory a přispěvatele (Jak přidat další látku)

Projekt se skládá z "chytrých" šablon (založených na knihovně DCLogic) a zdrojových dat v JSON.

**Postup přidání nového dokumentu:**
1. Nový soubor (PDF, HTML, DOCX) vložte do příslušné oborové složky (např. `/cnc/` nebo `/mte/`).
2. Otevřete soubor `site-structure.json` a přidejte k němu záznam do příslušného pole (např. `cncCards`). Zde se definuje název, který uvidí uživatel.
3. Pokud do budoucna přidáváte zcela nový obor, vytvořte pro něj novou složku obsahující `index.html` (zkopírujte z jiného oboru a upravte klíč v `s.{key}`) a zaregistrujte novou dlaždici do pole `home.cards` v `site-structure.json`.

*Vytvořeno a přizpůsobeno s ❤️ pro SPŠ a VOŠ Brno, Sokolská.*
