# ASCII Player

Trasforma un video in **arte ASCII a colori** e lo riproduce in una finestra, scritto in Python con OpenCV e NumPy.

## Funzioni

- Ogni frame viene convertito in caratteri colorati
- Finestra ridimensionabile
- Pausa con SPAZIO, uscita con Q / ESC / X della finestra
- Il video riparte da capo quando finisce
- Si può creare un `.exe` da condividere (senza mostrare il codice sorgente)

## Requisiti

- Python 3.8 o superiore
- Librerie in `requirements.txt`

## Installazione

```
git clone https://github.com/zakkukk/ascii-player.git
cd ascii-player
pip install -r requirements.txt
```

## Uso

Metti un video chiamato `video.mp4` nella cartella del progetto e avvia:

```
python ascii_player.py
```

Oppure indica un video qualsiasi:

```
python ascii_player.py percorso/del/mio_video.mp4
```

| Tasto | Azione |
|-------|--------|
| SPAZIO | pausa / riprendi |
| Q o ESC | chiudi |

## Impostazioni

In cima a `ascii_player.py` puoi modificare:

| Variabile | Significato |
|-----------|-------------|
| `CARATTERI` | caratteri usati, dal più scuro al più chiaro |
| `LARGHEZZA` | caratteri per riga (più alto = più dettaglio, più lento) |
| `LUMINOSITA` | rende i colori più o meno vivaci |

Consiglio: i risultati migliori si ottengono con video a sfondo scuro e soggetti colorati.

## Creare l'exe (Windows)

1. Metti `video.mp4` nella cartella del progetto
2. Installa PyInstaller:
   ```
   pip install pyinstaller
   ```
3. Crea l'exe:
   ```
   pyinstaller --onefile --noconsole --name ASCII-Player --add-data "video.mp4;." ascii_player.py
   ```
4. Troverai il file in `dist/ASCII-Player.exe`

Note:
- L'exe contiene già il video: basta condividere quel file
- L'antivirus potrebbe segnalarlo (succede spesso con PyInstaller): scegli "Esegui comunque"
- Se non si apre, rifai la build senza `--noconsole` per vedere gli errori

## Struttura del progetto

```
ascii-player/
├── ascii_player.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Nota sui video

Il video non è incluso nel repository. Usa video tuoi o con licenza libera: non pubblicare contenuti coperti da copyright.

