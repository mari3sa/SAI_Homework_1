# Break COLMAP

Mariateresa Mazzara | Matricola 2278680

Acquisizione e impostazioni. Foto scattate con Samsung Galaxy S22. Baseline: scarpa su cesto bianco, ripresa in ambiente interno lungo un giro; selezionate 20 viste dalle serie 22:19 e 22:21, con spaziatura approssimativa. Sottoinsiemi da 10, 5 e 3 immagini agli indici floor(i*20/n) dell’ordine circolare. Non è stata confermata l’immobilità tra le due serie. Sono state utilizzate le fotografie originali fornite dalla studentessa, conservate senza ulteriori ricompressioni.

COLMAP 4.2.1 (commit bd1fcf6), automatic_reconstructor, impostazioni geometriche predefinite, ricostruzione sparsa (--dense 0). Tutti i sei esperimenti usano CPU (--use_gpu 0) e due thread (--num_threads 2), dopo arresti software nelle esecuzioni GPU e CPU con parallelismo automatico. Ogni caso ha database e workspace indipendenti; gli arresti software preliminari sono esclusi dai risultati.

| Esperimento | Input | Registrate | Punti 3D | Esito |
|---|---:|---:|---:|---|
| Baseline | 20 | 20 | 11.560 | Un modello, sfondo e dispersione |
| Riduzione | 10 | 10 | 2.018 | Nuvola molto più rada |
| Riduzione | 5 | 3 | 51 | Frammento non riconoscibile |
| Riduzione | 3 | 0 | 0 | Nessun modello |
| Fallimento | 6 | 4 | 13 | Scena non ricostruita utilmente |
| Riparazione | 9 | 9 | 6.795 | Recupero parziale della struttura |

Riduzione delle viste. Tutti i casi con modello producono una sola componente. Passando da 20 a 10 viste i punti scendono da 11.560 a 2.018; con 5 restano 3 viste e 51 punti, con 3 nessun modello. Con 20 e 10 viste il profilo della scarpa è riconoscibile, insieme a punti di sfondo; con 5 resta un frammento non interpretabile. Il minor numero di viste aumenta i cambiamenti di aspetto tra immagini e riduce il supporto alle tracce. La registrazione completa non certifica la correttezza geometrica.

Fallimento intenzionale. Sei viste dei libri e del piano, seguendo un protocollo di rotazione quasi sul posto. Previsione salvata prima del run: feature e corrispondenze presenti, ma poca parallasse e inizializzazione/triangolazione instabile. Sono estratti 56.508 keypoint complessivi. Il log mostra difficoltà di inizializzazione e rilassamento automatico dei vincoli; il modello conservato ha solo 13 punti e 27 osservazioni. È un fallimento geometrico utile, non un crash. L’esito è coerente con scarsa parallasse, senza dimostrare rotazione perfettamente pura.

Riparazione. Aggiunte esattamente 3 foto con cambiamento di punto di vista, mantenendo le 6 iniziali e gli stessi parametri. Si ottengono 9/9 viste, 6.795 punti e 31.371 osservazioni; traccia media 4,62 e errore medio di riproiezione 1,065 px. Si distinguono fasce dei dorsi e parti del piano, ma persistono zone mancanti e punti dispersi. Il recupero è netto, la scena resta parziale. Accuratezza metrica e pose non sono verificate indipendentemente. Il precedente errore di soli 0,000016 px su 13 punti dimostra che un residuo basso da solo non prova una ricostruzione corretta.

Figure: baseline_clouds.png e repaired_clouds.png.
