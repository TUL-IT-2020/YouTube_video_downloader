# YouTube_video_downloader
15-20 stran

## Titulní strana

## Zadání

## Cíl projektu

Popsat problém.

Postup řešení
Nástroje
Řešení verze 1.
Uvažovaná řešení
Co nikam nevedlo

Řešení verze 2.
Odevzdávané řešení
### Uživatelský manuál
#### Instalace
Zdrojové kódy je možné stáhnout z GitHub repozitáře [zde](https://github.com/elPytel/YouTube_video_downloader). Pro instalaci na Linuxových strojích lze využít Bashový script uložený v adresáři Python. Po jeho spuštění se nainstalují všechny potřebné knihovny pro spuštění programu napsaného v jazyce Python.
#### Ovládání
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
## Vyhlídky do budoucna
## Zdroje
Při programování jsem čerpal z oficiální dokumentace jednotlivých Pythonovskcýh modulů, jejich příslušných GitHubových repozitářů a StackOverflow.


## TOD
- [ ] Ukládat navrhovaná slova
- [ ] Ukládat log

Vzorová generovaná slova
Často se v příkladu kdy nesedí jazyk videa k jeho názvu objevují strojově generované titulky, které za moc nestojí.