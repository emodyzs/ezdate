# ezdate
NLP modul for hungarian date-entity recognition and translation to specific date values\
NLP modul, magyar nyelvű dátum-kifejezések felismerése és lefordítása konkrét dátum-értékekre

## Telepítés
pip install ezdate

Előfeltétel:  Python 3.7 vagy későbbi

## Importálás
- from ezdate import ezdate\
   Hivatkozás: ezdate.text2date()
- from ezdate import ezdate as d\
   Hivatkozás: d.text2date()
- from ezdate.ezdate import text2date\
   Hivatkozás: text2date()

## Felhasználási terület
- NLP alkalmazások, dátumok kivonatolása, természetes nyelvi szófordulatok értelmezése
- chatbot alkalmazások

## Képességek
- relációs dátum-kifejezések értelmezése
- kontextuális időmeghatározások
- összetett, és akár többszörösen beágyazott dátum-kifejezéseket is képes kezelni
- kezeli a szövegesen megadott számokat, a római számokat, a sorszámokat, a ragokat és a dátumokkal kapcsolatos szinonim szófordulatokat is
- az egyedi dátumokon túlmenően dátum-tartományokat is fel tud ismerni

**Mit nem tud kezelni**:
- csak dátumbeazonosítás, napon belüli időszakokat és óra-perc időmeghatározásokat nem kezel
- korlátozott méretű (legfeljebb pár mondat terjedelmű) input kezelésére van optimalizálva

**Továbbfejlesztési lehetőségek**:
- legyen érzéketlen a hosszú és rövid ékezetek elírására
- a dátumszavak beazonosításakor engedjen meg kismértékű elgépeléseket is (fuzzy search)

## Példák
- 'jövő karácsony utáni második hétvégén'
- '2023 második féléve harmadik hetének elején'
- 'múlt hét péntek előtti három napon'
- 'a múlt század közepén',   'a 70-es évek elején'
- 'két év múlva októberben'
- 'két hónappal ezelőtt, 5-én'

  További példák az ezdate_teszt.py fájlban


## A modulhoz tartozó függvények
- **text2date()**:   ("Text to date") Magyar nyelvű időmeghatározások lefordítása dátumra vagy dátum tartományra


## Függvények részletezése

**text2date**( text, dt0=None, context='', outtype='first' ):
- **text**:  általában több szavas kifejezés vagy mondat
        A mondatban időhatározókon és számokon kívüli szavak is lehetnek (a dátum bárhol lehet a szövegen belül).
- **dt0**:  relációs dátummeghatározások esetén a kiinduló dátum.
        Ha nincs megadva, akkor a mai nap.
- **tense**: 'future' / 'past'.  A nem egyértelmű időmeghatározások esetén jövőbeli vagy múltbeli dátumot preferáljon a függvény
- **outtype**:
    - '**first**':    return =  '',   '2021.10.12',  '2021.12.10-2021.12.20'     Az első előforduló dátum vagy dátumtartomány.
    - '**first+**':   ugyanaz mint a first, de a string végére beírja a mintázatot és a helyettesőjelek kimeneti értékét is.
              Példa: '2021.10.12   pattern: [szám] [hónapnév] [szám]   outvalues: [2021, 'október', 'tizenkettedike']
    - '**all**':    '2021.10.12,2021.12.10-2021.12.20'
