def carica_da_file(file_path):  #codice, titolo, autore, mese, anno
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    listaPath = file_path.split("\\")
    # print(listaPath[-1])
    nomeFile=listaPath[-1]
    try:
        with open(nomeFile, "r") as inFile:
            inFile.readline()  # superiamo la prima riga d'intestazione
            album = {}
            for line in  inFile: # legge riga per riga fermandosi a ogni \n
                line = line.rstrip() # toglie '\n', line è un'unica stringa
                parole = line.split(',') # otteniamo una lista con le parole della riga ordinate
                # ora aggiorniamo il dizionario
                anno = parole[-1]
                codiceFoto = parole[0]
                info = parole[1:]
                if anno not in album:
                    album[anno] = {}
                album[anno][codiceFoto] = info
            print('album registrato correttamente')
            return album

            # prova stampa album
            #for item in album.items():
            #    print(item)

    except FileNotFoundError: # gestione errore
        print("File non trovato")
        return None



def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path): #codice, titolo, autore, mese, anno
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    anno = str(anno) # le chiavi hanno il formato str
    if anno not in album:
        album[anno] = {}
    album[anno][codice] = [titolo,autore,mese,anno]

    #prova stampa foto
    # print(f"hai in inserito nell'album:\n {codice} {album[anno][codice]}")

#aggiornamento file di partenza
    listaFile = file_path.split("\\")
    nomeFile = listaFile[-1]
    file = open(f'{nomeFile}', 'a') # 'a' sta per append, 'w' cancella il file su cui lavori, entrambi in assenza di file ne inizializzano uno
    file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    file.close()    # salva le modifiche, ma non dà errore se non presente

    return album    # in questo modo aggiorniamo la struttura dati nel main() con due sole righe di codice


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for anno in album:
        if codice in album[anno]:
            info = album[anno][codice]
            foto = [codice] + info
            # prova output coerente con quello iniziale
            # print(foto)
            return foto
    return None # gestione errore



def elenco_foto_anno_per_titolo(album, anno): #codice, titolo, autore, mese, anno
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    anno = str(anno)
    if anno not in album:
        foto_ordinate = None # gestione errore
    else:
        foto_anno = album[anno]      # scelto l'anno restituisce tutte le foto corrispondenti   # dict                  crea un nuovo dizionario
        codice_foto_ordinate = dict(sorted(foto_anno.items(), key=lambda item: item[1][0]))     # foto_anno.items()     trasforma tutti gli elementi del dzionario in una tupla a due elementi (codice, [info])
                                                                                            # key=lambda            indica la regola di ordinamento, ovvero [1] secondo elemento della tupla e [0] primo elemento: titolo
        foto_ordinate = []      # associamo i codici ordinati al titolo della foto corrispondente
        for cod in codice_foto_ordinate:
            foto = []
            foto.append(cod)
            foto.append(album[anno][cod])
            foto_ordinate.append(foto)

    return foto_ordinate #(forse più efficiente stampare chiave e contenuto direttamente nel main)


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())      # accetta anche numeri > 12
                anno = int(input("Anno: ").strip())     # utile per verifica dei dati
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            album = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            anno = str(anno)            # la chiave richiede una stringa, dunque si converte il dato
            foto = album[anno][codice]
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                print('anni disponibili:')
                for anno in album:
                    print(anno)
                anno = int(input("Inserisci l'anno da consultare: ").strip())   #risolvibile anche indicando l'imput come una stringa
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
