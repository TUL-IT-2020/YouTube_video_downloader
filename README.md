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

Aplikace má stahovat videa dle volby poptávaného jazyka. A to tak, že pokud možno rychle a s co nejvyšší shodou jazyka záznamu a titulků. Účelem výsledné aplikace je vytěžování audio dat s přepisem řeči pro další využití v úlohách strojového učení, jako jsou rozpoznání slov a automatický převod řeči na text. V těchto úlohách je žádoucí mít co nejvíce trénovacích dat. YouTube je jednou z největších volně přístupných databází videí a značné procento z nich má dokonce autorem vytvořené titulky. Vzhledem k těmto charakteristikám se YouTube stal vhodným kandidátem pro zdroj surových dat.

Má práce spočívala ve vytvoření programu, který po konfiguraci a zadání jazyka začne prohledávat Youtube a stahovat všechna vhodná videa. Mezi klíčové problémy, které jsem při vývoji musel překonat spadalo: 
- vyhledávání videí v požadovaném jazyce
- odhadnutí jazyka videa pro prvotní kontrolu
- selekce nahrávek bez titulků v požadovaném jazyce
- stáhnutí videa a titulků
- převod videa na pouhý audio záznam

## Využité nástroje:
### Metody TDD & extrémního programování
Testy řízené programování. Zde bylo využito knihovny [pytest](#pytest). Ve výsledku je aplikace pokryta testy pouze z nějakých 30%. To sice není mnoho, ale testují se základní funkce a logika aplikace. Pro větší pokrytí by bylo potřeba vytvoření mock tříd pro integrační testy komunikace programu s YouTube.

### TUI - terminal user interface
Aplikace je vybavená konzolovým aplikační rozhraní. Parsovaná přepínačů je zprostředkováno knihovnou [argparse](#argparse), která umožňuje zadávání argumentů v libovolném pořadí a automaticky generuje help výpis.

### Více vláknové programování
Aplikace využívá rozdělení do více vláken za pomocí standardního modulu [threading](#threading). V hlavním vláknu programu je řešeno čtení z konzole ("q" pro ukončení aplikace). Worker thread řeší veškerou zbylou logiku programu.

### Vyhledávání videí
Pro vyhledávání videí byla použita knihovna [youtubesearchpython](#youtubesearchpython). Velkou výhodou využití této knihovny oproti parsování informací přímo z YouTube je možnost listování na další stránky výsledků, které je na stránkách dnes řešeno pomocí responzivního webu, které je takřka nemožné obejít pomocí jednoduchého web crawleru. 

### Detekce jazyka
Jazyk z jednotlivých textů aplikace rozpoznává s využitím modulu [langdetect](#langdetect). Jeho velkou výhodou je jednoduché použití. Pro detekci jazyka stačí zavolat funkci `langdetect.detect_langs(text)` a ta vrátí list všech možných detekovaných jazyků s procentuální pravděpodobností.

### Práce s titulky
Po experimentování s několika knihovnami určenými pro práci s YouTube titulky vyvstala knihovna [youtube_transcript_api](#youtube_transcript_api) jako ideální volba. Zejména díky snadnému dotazování na seznam jazyků použitých titulků a možnost stáhnutí dat jak ve formátu s časovou značkou, tak i čistě jako pouhý text. V obou případech je výstup uložen do souboru .txt (prostý text). Zde jiné knihovny umožňovali uložení pouze v proprietárních formátech, jenž byli vyhodnoceny jako nevhodné s ohledem pro další zpracování. 

### Stahování videí
To je zajištěno funkcionalitami v modulu [yt_dlp](#yt_dlp). Původně byl vnitřní algoritmus aplikace postaven na knihovně [youtube-dl](https://github.com/ytdl-org/youtube-dl), ale YouTube nejspíše nebyl smířen s jejím velkým rozšířením pro automatické stahování videí a proto zavedl opatření, která omezila rychlost stahování na ~300kbps, která je pro získávaní velkého objemu dat naprosto nepoužitelná. Tento problém naštěstí obchází výše zmíněná knihovna yt_dlp a díky tomu že je forkem youtube-dl (vychází z jejích zdrojových kódů), tak se při přechodu ani nemění aplikační interface a je možné použít všechny funkce tak jako by se jednalo o původní knihovnu. 
Knihovna také umožňuje převedení formátu videa po dokončení jeho stahování. Aplikace je tak může hned po uložení automaticky převést do formátu .wav.  

## Postup řešení
### Řešení v Bashi
Zprvu byl pro řešení zvolen skriptovací jazyk Bash. Ten má mnoho výhod, umožňuje volat konzolové programy, jako kdyby to byli jeho funkce a díky tomu lze snadno získat pokročilé možnosti. Mezi ně například patří stažení videa či audia pomocí programu youtube-dl zapsaného na jeden řádek. V Bashi je také snadné vytvořit vysoce paralelní aplikaci pomocí spouštění podprocesů řešící jednotlivé dílčí úkony. Velmi lehká je také práce s adresáři a soubory, jelikož základní příkazová výbava Bashe je tvořena nástroji pro ovládání počítače z terminálu, což obnáší pohyb adresářovou strukturou, mazání a vytváření souborů, jejich výpis a další. 

Při návrhu algoritmu bylo provedeno rozhodnutí rozdělit problém na dvě části:
Nejprve prohledat YouTube a vytvořit databázi o co největším počtu záznamů, které by tvořil formát:
- id videa
- id kanálu
- název videa
- jazyk videa
- seznam jazyků dostupných titulků
- A ve poslední řadě také záznam o všech našeptávaných videích na stejné stránce.

A ve druhém kroku napsat ještě jiný program, který by po zadání již specifického jazyka databázi prohledal a stáhl všechna uložená videa která splní kriteria (videa s titulky).
Výhodou tohoto řešení by bylo opakované využití záznamů z prvního kroku pro hledání různých jazyků.

Při implementaci nastalo rovnou několik nečekaný problémů.
První při analýze dat.
Když byl dokončen kód k prohledávání YouTube a ukládání záznamů o 
videích. A část skriptů pro práci s youtube-dl byla rozpracována do takové úrovně, že se již podařilo stahovat jak záznam videa převedeného do formátu .wav, tak i titulky. 
Program byl nechán běžet přes víkend a zvládl stáhnout něco přes 200k záznamů. Při jejich podrobnějším prozkoumání byl zvolen jazyk Čeština pro snadnou validaci dat. Počet vyfiltrovaných videí splňujících kriterium českých titulek byl přibližně ~350, to se nejevilo zas tak zle, jenže u žádného z nich se nevyskytoval český název, co více, tak naprostá většina z nich měla názvy v úplně cizích abecedách. 
Co říci, do algoritmu byla vložena větší naději na úspěch. Problém byl patrně v tom, že youtube algoritmus si pamatoval všechna předchozí dotazování a při prohledávání do hloubky, padal čím dál tím víc do zaječí nory. 

Druhý problém byl při samotném běhu programu. 
Dotazování na servery YouTubu vytěžovalo počítač více, než byl prvotní předpoklad. Tím důvodem se patrně stal zvolený programovací jazyk, který nikdy nebyl zamýšlen pro časově kritické úkoly a tak interpretovaný Bash byl prostě pro danou úlohu příliš pomalý a paměťově náročný.

Pod tíhou dosavadních výsledků a s vyplýtvanou více než polovinou časové dotace pro řešení úkolu bylo učiněno nelehké rozhodnutí. A to opustit dosavadní práci a začít sice od znova, avšak vydat se naprosto jinou cestou, jenž se snad, jak se ukáže s odstupem času, také nebude jevit slepou.

### Řešení v Pythonu
Vzhledem k tomu, že předchozí řešení nepřineslo uspokojivé výsledky, byl nový zvolený směr založen na změně programovacího jazyka, přechod na Python, a také změně přístupu. Místo vytvoření databáze videí s titulky stejně tak jako bez titulků určené pro další filtrování, bylo rozhodnuto dát velký důraz na seed vyhledávání. Nový algoritmus si kladl za cíl nejdříve vytvořit dotaz v kýženém jazyce a poté vyselektovat všechny videa s titulky a ty stáhnout.
Vytvoření dotazu
Vyhledávání videí v požadovaném jazyce
detekce jazyka
selekce nahrávek bez titulků v požadovaném jazyce

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
- ***verbose*** pro podrobnější výpisy do konzole
- ***debug*** přidání debugovacích hlášení
- ***EN*** pro vyhledávání se zvolí angličtina
- ***words***, počet náhodně vygenerovaných slov bude 4
- ***iterations***, počet vyhodnocených výsledků každého dotazu bude 100

### Další jazyky
Jazyk se vybírá pomocí dvoupísmenného kódu ISO 639-1. Seznam kódů k jednotlivým jazykům: [zde](https://www.science.co.il/language/Codes.php). Pro přidání dalšího jazyka do aplikace je zapotřebí stáhnout wordlist ve formátů .txt a kódování UTF-8, ze kterého se budou generovat náhodná slovní spojení a ten uložit do adresáře **dict/**. Dále je potřeba aktualizovat konfigurační soubor **Python/languages.json**.

Vzorový záznam:
```JSON
{
	"CS": {
		"title": "Czech",
		"code": "cs",
		"file_name": "czech.txt"
	}
}
```

## Analýza výsledků
Rychlost a úspěšnost
Tabulka 

cca 30-100 souborů
Jazyky k analýze:
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
Použité knihovny:
- <a name="pytest"></a>[pytest](https://pypi.org/project/pytest/)
- <a name="argparse"></a>[argparse](https://pypi.org/project/argparse/)
- <a name="threading"></a>[threading](https://docs.python.org/3/library/threading.html)
- <a name="youtubesearchpython"></a>[youtubesearchpython](https://pypi.org/project/youtube-search-python/)
- <a name="langdetect"></a>[langdetect](https://pypi.org/project/langdetect/)
- <a name="youtube_transcript_api"></a>[youtube_transcript_api](https://pypi.org/project/youtube-transcript-api/)
- <a name="yt_dlp"></a>[yt_dlp](https://pypi.org/project/yt-dlp/)

## Přílohy
- [Tabulka analýza CZ](https://htmlpreview.github.io/?https://github.com/elPytel/YouTube_video_downloader/blob/main/doc/CS.html)
- [Tabulka analýza SK](https://htmlpreview.github.io/?https://github.com/elPytel/YouTube_video_downloader/blob/main/doc/SK.html)
- [Tabulka analýza EN](https://htmlpreview.github.io/?https://github.com/elPytel/YouTube_video_downloader/blob/main/doc/EN.html)

## TODO
- [ ] Ukládat navrhovaná slova
- [ ] Ukládat log

Vzorová generovaná slova
Často se v příkladu kdy nesedí jazyk videa k jeho názvu objevují strojově generované titulky, které za moc nestojí.