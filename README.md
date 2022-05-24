# YouTube_video_downloader
## Tvorba trénovacích dat pro strojové učení ze záznamů na Youtube
15-20 stran
Osnova:
1. Název (český i anglický), jméno autora a vedoucího, rok vypracování.
2. Zadání.
3. Anotace česká i anglická s klíčovými slovy.
4. Úvod – stručné vysvětlení řešené problematiky, souvislost s praxí, stanovení cílů.
5. Popis použitých metod (prostředků, obvodů, algoritmů, apod. s odkazy na literaturu), je
nepřípustné opisovat texty či kopírovat obrázky z literatury bez řádné citace.
6. Vlastní řešení konkrétního problému, tj. popis vlastních prací, výsledků apod.
7. Shrnutí výsledků projektu a závěr (naznačení dalšího možného pokračování).
8. Použitá literatura.

## Titulní strana

## Zadání

## Úvod
Cílem mé práce bylo provést studii proveditelnost pro aplikaci, jenž by automaticky stahovala videa s titulky z webové platformy YouTube. 

Aplikace má stahovat videa dle volby poptávaného jazyka. A to tak, že pokud možno rychle a s co nejvyšší shodou jazyka záznamu a titulků. Účelem výsledné aplikace je vytěžování audio dat s přepisem řeči pro další využití v úlohách strojového učení, jako jsou rozpoznání slov a automatického převodu řeči na text. V těchto úlohách je žádoucí mít co nejvíce trénovacích dat. YouTube je jednou z největších volně přístupných databází videí a značné procento z nich má dokonce autorem vytvořené titulky. Vzhledem k těmto charakteristikám se YouTube stal vhodným kandidátem pro zdroj surových dat.

Má práce spočívala ve vytvoření programu, který po konfiguraci a zadání jazyka začne prohledávat Youtube a stahovat všechna vhodná videa. Mezi klíčové problémy, které jsem při vývoji musel překonat spadalo: 
- vyhledávání videí v požadovaném jazyce
- odhadnutí jazyka videa pro prvotní kontrolu
- selekce nahrávek bez titulků v požadovaném jazyce
- stáhnutí videa a titulků
- převod videa na pouhý audio záznam

## Nástroje:
import langdetect
from youtube_transcript_api import YouTubeTranscriptApi as YTTA
import yt_dlp
from youtubesearchpython
### Metody TDD & extrémního programování
Testy řízené programování. Zde bylo využito knihovny [pytest](#pytest). Ve výsledku je aplikace pokryta testy pouze z nějakých 30%. To sice není mnoho, ale pokrývá to základní logiku a funkce aplikace. Pro větší pokrytí by bylo potřeba vytvoření mock tříd pro integrační otestování komunikace programu s YouTube.

### Více vláknové programování
threading
### TUI - terminal user interface
Konzolové aplikační rozhraní.
argparse

## Postup řešení
### Řešení v Bashi
Řešení verze 1.
Uvažovaná řešení
Co nikam nevedlo

### Řešení v Pythonu
Řešení verze 2.
Odevzdávané řešení


## Uživatelský manuál
### Instalace
Zdrojové kódy je možné stáhnout z GitHub repozitáře [zde](https://github.com/elPytel/YouTube_video_downloader). Pro instalaci na Linuxových strojích lze využít Bashový script uložený v adresáři Python. Po jeho spuštění se nainstalují všechny potřebné knihovny pro spuštění programu napsaného v jazyce Python.
### Ovládání
Aplikace disponuje pouze terminálovým rozhraním. Jednotlivé volby programu se zadávají pomocí přepínačů při spuštění. Jejich zpracování je provedeno pomocí standardního modulu **argparse**, díky tomu je vstup poměrně robustní a nezáleží na pořadí zadaných přepínačů. 
Výpis z konzole pro volbu *-h* "help":
```Bash
$ python3 main.py -h
usage: main.py [-h] [-l LANGUAGE] [-w WORDS] [-i ITERATIONS] [-v]
               [-d]

Youtube video & subtitles downloader.

options:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        select language
  -w WORDS, --words WORDS
                        Set number of generated words.
  -i ITERATIONS, --iterations ITERATIONS
                        Number of tested iterations for query
  -v, --verbose         Increase verbosity.
  -d, --debug           Run debug options.
```

Příklad spuštění v základní konfiguraci a s volbou českého jazyka (soubor main.py se nachází v adresáři **Python/**):
```Bash
$ python3 main.py -l CS
```

Pokročilá volba s angličtinou:
```Bash
$ python3 main.py -v -d -l EN -w 4 -i 100
```
Provede se nastavení: 
- *verbose* pro podrobnější výpisy do konzole
- *debug* přidání debugovacích hlášení
- *EN* pro vyhledávání se zvolí angličtina
- *words*, počet náhodně vygenerovaných slov bude 4
- *iterations*, počet vyhodnocených výsledků každého dotazu bude 100

### Další jazyky
Jazyk se vybírá pomocí dvoupísmenného kódu ISO 639-1. Seznam kódů k jednotlivým jazykům: [zde](https://www.science.co.il/language/Codes.php). Pro přidání dalšího jazyka do aplikace je zapotřebí stáhnout wordlist ve formátů .txt a kódování UTF-8, ze kterého se budou generovat náhodná slovní spojení a ten uložit do adresáře **dict/**. Dále je potřeba aktualizovat konfigurační soubor **Python/languages.json**.

## Analýza výsledků
Rychlost a úspěšnost
Tabulka 

cca 30-100 souborů
Jazyky k analíze:
Projít ručo/algoritmicky
Češtině, Slověnština, Němčina, Angličtina
Bez analízy:
Noršitna Švédština


analýza funkčnosti
tabulka
česke, české video
neni česke, česke video
české vide, titulky nejsou česke .....
jazyk v češtině, titulky v češtině, nesouhlasí
ǔspšnost na češtině taková a taková

## Závěr
### Možné rozšíření do budoucna
Přidání detekce jazyka ze zvukové stopy. Grafická nadstavba konzole. Vícevláknová implementace části kódu dedikovaného pro stahování a zpracování videí pro urychlení běhu kódu na vícevláknových platformách. Možnost upravit hranici rozpoznání na bázi jednotlivých jazyků.

## Zdroje
Při programování jsem čerpal z oficiální dokumentace jednotlivých Pythonovských modulů, jejich příslušných GitHubových repozitářů a StackOverflow.

<a name="pytest"></a>[pytest](https://pypi.org/project/pytest/)

## TOD
- [ ] Ukládat navrhovaná slova
- [ ] Ukládat log

Vzorová generovaná slova
Často se v příkladu kdy nesedí jazyk videa k jeho názvu objevují strojově generované titulky, které za moc nestojí.