"""
ASCII Player (alta qualità)
Trasforma un video in arte ASCII a colori e lo mostra in una finestra.

Uso:
    python ascii_player.py              (usa video.mp4 nella cartella)
    python ascii_player.py mio_video.mp4

Comandi:
    Q o ESC  -> chiudi
    SPAZIO   -> pausa / riprendi
    F        -> schermo intero / finestra
"""

import cv2
import numpy as np
import sys
import os
import time

# ---------- IMPOSTAZIONI (puoi modificarle) ----------
# 70 caratteri: più sono, più i passaggi di luce sono morbidi
CARATTERI = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
LARGHEZZA = 160            # caratteri per riga (più alto = più dettaglio, più pesante)
CELLA_L = 8                # larghezza di un carattere in pixel
CELLA_A = 12               # altezza di un carattere in pixel
FONT_SCALA = 0.4           # grandezza del carattere dentro la cella
LUMINOSITA = 1.2           # moltiplicatore dei colori (1.0 = originali)
NOME_FINESTRA = "ASCII Player"
# -----------------------------------------------------


def percorso(nome):
    # quando il programma è un exe, i file sono in una cartella temporanea
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nome)
    return nome


def crea_glifi():
    # disegno ogni carattere in una piccola immagine (bianco su nero)
    immagini = []
    for c in CARATTERI:
        img = np.zeros((CELLA_A, CELLA_L), dtype=np.uint8)
        if c != " ":
            cv2.putText(img, c, (0, CELLA_A - 3), cv2.FONT_HERSHEY_SIMPLEX,
                        FONT_SCALA, 255, 1, cv2.LINE_AA)
        immagini.append(img)
    immagini = np.array(immagini)

    # misuro quanto "inchiostro" ha ogni carattere e li ordino dal più vuoto al più pieno
    densita = immagini.reshape(len(CARATTERI), -1).mean(axis=1)
    ordine = np.argsort(densita)
    immagini = immagini[ordine]
    densita = densita[ordine]
    densita = densita / densita.max()   # da 0 a 1

    # tabella: per ogni luminosità (0-255) il carattere con la densità più vicina
    tabella = np.zeros(256, dtype=np.int32)
    for i in range(256):
        tabella[i] = np.argmin(np.abs(densita - i / 255.0))

    return immagini, tabella


def frame_in_ascii(frame, glifi, tabella):
    # 1) riduco il frame: un pixel = un carattere (INTER_AREA fa la media, qualità migliore)
    altezza = int(frame.shape[0] / frame.shape[1] * LARGHEZZA * CELLA_L / CELLA_A)
    piccolo = cv2.resize(frame, (LARGHEZZA, altezza), interpolation=cv2.INTER_AREA)

    # 2) scelgo il carattere in base alla luminosità (il canale più forte del pixel)
    v = piccolo.max(axis=2)
    indici = tabella[v]

    # 3) unisco le immagini dei caratteri scelti in un'unica maschera
    celle = glifi[indici]                       # forma: (righe, colonne, A, L)
    celle = celle.transpose(0, 2, 1, 3)         # (righe, A, colonne, L)
    maschera = celle.reshape(altezza * CELLA_A, LARGHEZZA * CELLA_L)

    # 4) colori più vivaci: la luminosità la danno già i caratteri
    v_float = np.maximum(v, 1).astype(np.float32)[:, :, None]
    colori = piccolo.astype(np.float32)
    colori = colori * 0.4 + colori * (255.0 / v_float) * 0.6
    colori = np.clip(colori * LUMINOSITA, 0, 255).astype(np.uint8)

    # 5) ingrandisco i colori e li applico ai caratteri
    colori = cv2.resize(colori, (LARGHEZZA * CELLA_L, altezza * CELLA_A),
                        interpolation=cv2.INTER_NEAREST)
    maschera = cv2.merge([maschera, maschera, maschera])
    return cv2.multiply(colori, maschera, scale=1.0 / 255.0)


def main():
    # scelgo il video: quello passato da riga di comando oppure video.mp4
    if len(sys.argv) > 1:
        file_video = sys.argv[1]
    else:
        file_video = percorso("video.mp4")

    video = cv2.VideoCapture(file_video)
    if not video.isOpened():
        print("Errore: impossibile aprire il video '" + file_video + "'")
        input("Premi INVIO per uscire...")
        return

    fps = video.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    durata_frame = 1.0 / fps

    glifi, tabella = crea_glifi()
    cv2.namedWindow(NOME_FINESTRA, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)

    in_pausa = False
    schermo_intero = False
    immagine = None
    prima_volta = True

    while True:
        inizio = time.time()

        if not in_pausa:
            ok, frame = video.read()
            if not ok:
                # il video è finito: riparte da capo
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            immagine = frame_in_ascii(frame, glifi, tabella)

            if prima_volta:
                # la finestra parte con una dimensione comoda
                cv2.resizeWindow(NOME_FINESTRA, 1280, int(1280 * immagine.shape[0] / immagine.shape[1]))
                prima_volta = False

        cv2.imshow(NOME_FINESTRA, immagine)

        # aspetto il tempo che manca per rispettare gli fps del video
        trascorso = time.time() - inizio
        attesa = max(1, int((durata_frame - trascorso) * 1000))
        tasto = cv2.waitKey(attesa) & 0xFF

        if tasto == ord("q") or tasto == 27:    # Q oppure ESC
            break
        if tasto == ord(" "):                   # SPAZIO
            in_pausa = not in_pausa
        if tasto == ord("f"):                   # F
            schermo_intero = not schermo_intero
            if schermo_intero:
                cv2.setWindowProperty(NOME_FINESTRA, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            else:
                cv2.setWindowProperty(NOME_FINESTRA, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

        # chiusura con la X della finestra
        if cv2.getWindowProperty(NOME_FINESTRA, cv2.WND_PROP_VISIBLE) < 1:
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
