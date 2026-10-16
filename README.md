# Homework 1 - Break COLMAP

Stato: struttura pronta; esperimenti non eseguiti, in attesa delle foto originali e di COLMAP.
Scadenza della traccia: 17 ottobre 2026, 23:59 CEST.

## Materiale necessario

- Nome, cognome e matricola.
- 20 foto originali dello stesso oggetto statico, scattate in ordine attorno ad esso.
- Da 2 a 10 foto originali per un caso deliberatamente difficile.
- Da 1 a 3 foto aggiuntive dello stesso caso per il tentativo di riparazione.
- COLMAP per Windows: https://colmap.github.io/install.html . Verificare `COLMAP.bat -h` e conservare la versione effettiva.
- Python 3 (lo script usa solo la libreria standard).

## Piano degli scatti

1. Baseline: scegli una scarpa o un oggetto con texture, illuminazione diffusa e sfondo statico. Muovi il telefono attorno all'oggetto con circa 20 posizioni equidistanti, mantenendo sovrapposizione. Non ruotare l'oggetto. Evita riflessi, ritratto, zoom variabile e mosso. Copia gli originali via cavo in `originals/baseline`.
2. Fallimento: fotografa una scena statica ricca di dettagli ruotando il telefono quasi sul posto, con centro ottico il piu possibile fermo e viste sovrapposte (per esempio 6 foto). Foto nitide e ben esposte. Scrivi la previsione in `report/relazione.md` PRIMA di eseguire questo caso. La rotazione pura e approssimativa: piccoli spostamenti involontari possono produrre una ricostruzione parziale; non considerare garantito il fallimento.
3. Riparazione: aggiungi 3 foto della stessa scena spostandoti lateralmente, con sovrapposizione alle viste precedenti e senza muovere oggetti. Copiale in `originals/repair_extra`. Useremo le foto aggiunte come unico intervento, mantenendo le impostazioni predefinite.

Se i file non sono gia ordinati lessicograficamente per acquisizione, crea `baseline_order.txt`: un nome file originale per riga, nell'ordine del giro. Lo script copia i file byte per byte, senza ricompressione.

## Esecuzione dal terminale VS Code

```powershell
python workflow.py prepare
python workflow.py run --colmap "C:\percorso\COLMAP.bat"
python workflow.py zip
```

`prepare` crea sei cartelle indipendenti in `experiments`, piu un manifest con hash SHA-256. Rifiuta di sovrascrivere esperimenti esistenti. I sottocampioni sono distribuiti sul giro completo (indici floor(i*20/n)).

`run` usa `automatic_reconstructor` con i default e `--dense 0` per limitarsi alla ricostruzione sparsa ammessa dalla traccia. Registra comandi, help/versione e log. Non modifica soglie o algoritmi. I run gia avviati non vengono sovrascritti. `results.json` riporta conteggi per ogni componente: componenti separate non vanno sommate come se fossero un unico modello coerente. Un errore del programma e distinto dall'assenza di modello.

Apri ogni modello con COLMAP per controllare forma, camere, punti fuori posto e componenti separate; salva screenshot in `report`. Il numero di punti da solo non dimostra correttezza. Completa la relazione con osservazioni reali, seleziona foto e screenshot, quindi esporta in PDF: massimo due pagine di testo o circa 6000 caratteri, figure e tabelle escluse.

`zip` crea `submission/original_images.zip` senza compressione ZIP e senza alterare immagini. Il PDF finale deve essere aggiunto dopo gli esperimenti. Non consegnare la bozza con campi mancanti.

Documentazione CLI: https://colmap.github.io/cli.html
