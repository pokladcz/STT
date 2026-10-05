# Design Spec: Výukový portál Strojírenství

## 1. Účel a Kontext
Cílem je transformovat existující interaktivní repozitář pro předmět STT na komplexní výukový portál pro strojírenské předměty. Portál bude sloužit studentům a učitelům na **Střední průmyslová škola a Vyšší odborná škola Brno, Sokolská, příspěvková organizace**.

## 2. Architektura a Uživatelské Rozhraní

### 2.1. Úvodní stránka (Rozcestník)
- **Název projektu:** Strojírenství.
- **Obsah první strany:** Grafický rozcestník (výběr) všech dostupných předmětů (STT, SPS, MEC, Robotika, CNC, MTE). Uživatel po vstupu na web vidí jasně oddělené dlaždice/odkazy na jednotlivé obory.

### 2.2. Navigace a Vyhledávání
- **Vyhledávání:** V horní části stránky (top bar) bude umístěno globální vyhledávací pole, které umožní fulltextové nebo indexované vyhledávání napříč všemi předměty a materiály.
- **Hlavní menu:** Bude sloužit pro rychlé přepínání mezi předměty. Uvnitř předmětu pak bude lokální menu kapitol.

## 3. Integrace Dat (Složka 1-skola)

### 3.1. Zpracování souborů
- Existující obsah STT bude logicky seskupen pod předmět STT (struktura složek jako `koroze`, `odlevani` se stane podkategoriemi STT).
- Skript generující web (např. `sync.py`) se upraví nebo rozšíří tak, aby dokázal vzít materiály (PDF, HTML) ze zdrojové složky `1-skola` a aplikovat na ně existující šablony.
- Každý nový předmět dostane vlastní `index.html` a položku v konfiguračním JSON souboru (`site-structure.json`).

## 4. README.md

Struktura repozitáře dostane nový dokumentační soubor sestávající z:
- **Hlavička:** Jasná deklarace, že se jedná o výukový portál pro **SPŠ a VOŠ Brno, Sokolská**.
- **Pro studenty:** Návod k použití portálu (jak vyhledávat materiály, tipy pro zobrazení přes F11 pro lepší čitelnost diagramů).
- **Pro učitele:** Tipy pro integraci do výuky (prezentování diagramů, interaktivních prvků).
- **Pro přispěvatele:** Technický návod, jak upravovat JSON strukturu a přidávat nové kapitoly.

## 5. Úprava generátoru (Technický dluh)
- Původní `sync.py` je hardcodovaný na aktuální sadu stránek STT. Bude potřeba ho buď parametrizovat pro dynamické čtení z podadresářů předmětů, nebo napsat pre-build krok, který dynamicky sestaví `site-structure.json` z obsahu.

## Zhodnocení Scope
Tento návrh je ucelený, realizovatelný a řeší všechny požadavky bez zbytečných externalit. Neobsahuje žádné nejasnosti. Všechny zmíněné entity (vyhledávání, rozcestník, data ze složky) jsou adresovány.