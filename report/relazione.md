# Break COLMAP - bozza da completare con risultati reali

Nome: DA COMPILARE | Cognome: DA COMPILARE | Matricola: DA COMPILARE

Versione COLMAP: DA VERIFICARE. Ricostruzione automatica, impostazioni predefinite; solo ricostruzione sparsa (dense=0). Riparazione mediante aggiunta di immagini, nessuna modifica ai parametri.

## Acquisizione e riduzione delle viste

DA COMPILARE: oggetto, telefono, disposizione e illuminazione. Selezione uniforme delle viste lungo il percorso di acquisizione.

| Esperimento | Input | Registrate (per componente) | Punti 3D (per componente) | Correttezza visiva |
|---|---:|---|---|---|
| Baseline | 20 | da misurare | da misurare | da osservare |
| Sottoinsieme | 10 | da misurare | da misurare | da osservare |
| Sottoinsieme | 5 | da misurare | da misurare | da osservare |
| Sottoinsieme | 3 | da misurare | da misurare | da osservare |
| Fallimento | da misurare | da misurare | da misurare | da osservare |
| Riparazione | da misurare | da misurare | da misurare | da osservare |

Spunti da verificare sui risultati: meno viste possono ridurre sovrapposizione, corrispondenze robuste e lunghezza delle tracce, mentre aumentano i cambiamenti di aspetto. Il fallimento dipende dalla scena: non esiste un numero universale di immagini sufficiente. Descrivere dove si osserva effettivamente il degrado.

## Fallimento intenzionale

Previsione DA SALVARE PRIMA DEL RUN: con rotazione quasi pura possono esistere feature e match, ma la mancanza di baseline limita la parallasse e rende la triangolazione della profondita degenere o instabile. Ci si aspetta difficolta di inizializzazione/ricostruzione geometrica, non necessariamente nell'estrazione di feature.

Risultato osservato: DA COMPILARE dai log e dall'ispezione del modello. Separare un errore software da un fallimento geometrico. Discutere eventuali piccoli spostamenti involontari della camera.

## Riparazione e verifica

Intervento previsto: aggiunta di massimo 3 immagini con traslazione e sufficiente sovrapposizione. Risultato: DA COMPILARE. Confrontare registrazione, geometria e posizioni delle camere con la scena reale; un modello esistente puo essere distorto o frammentato. Non dedurre accuratezza metrica senza una misura di riferimento.

## Figure da inserire

Alcune foto originali rappresentative e screenshot delle ricostruzioni, con didascalie che identifichino l'esperimento. In caso di nessun modello, documentare l'esito tramite log, senza inventare una ricostruzione.
