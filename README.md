# Last-Mile-Problem
Il problema dell'ultimo miglio, noto anche come "last mile problem" in inglese, è una sfida logistica che si presenta nelle reti di distribuzione di merci. 
Abbiamo modellizzato un’ipotetica mappa e calcolare il percorso più breve per effettuare le consegne richieste. Il centro di distribuzione sarà il nostro punto di partenza e di arrivo.
Per risolvere il problema abbiamo usato parallelamente PDDL e algoritmi di search, valutando le rispettive velocità di risoluzione.

## Algoritmi di SEARCH
Per il corretto funzionamento dell'applicazione è necessario aver installato la libreria igraph, con la quale viene gestito il grafo che rappresenta la mappa.
Inserire i file .py e i file .json in un'unica directory.

Per far partire l'applicazione è necessario avviare il file 'main.py' e che sia presente un file di configurazione con i parametri del problema.
Il file di configurazione deve essere nella sessa cartella del file 'main.py' e di tutti gli altri file .py.

### Configurazione
Il file di configurazione prevedere i seguenti campi:
- 'init': lo stato iniziale da cui deve partire e deve terminare il percorso
- 'goal': una lista di stati attraverso cui deve transitare l'agente
- 'size': la dimensione che deve avere il mondo. Per mappe inserite dall'utente questo dato è irrilevante, ma per i mondi generati dall'applicazione è fondamentale
- 'world_type': il tipo di mondo. 3 possibilità:
    - 'fixed': la mappa è inserita dall'esterno attraverso un file 'mappa.json'
    - 'random': una mappa creata casualmente con distanze casuali, per questa mappa 'size' indica il numero di location presenti
    - 'square': una mappa quadrata con distanze casuali, per questa mappa 'size' indica la dimensione del lato, ci saranno quindi 'size'*'size' location
- 'solvers': una lista di algoritmi di ricerca con cui si vuole trovare una soluzione. Attualmente gli algoritmi disponibili sono
    - 'BestFirstSearch': ricerca a costo uniforme
    - 'BFS': ricerca in ampiezza
    - 'DLFS': ricerca a profondità limitata
    - 'IterativeSearch': ricerca ad approfondimento iterativo
- 'folder_path': il percorso di una directory in cui salvare i risultati dell'esecuzione

Attualmente per la generazione delle mappe casuali il numero massimo delle location è 26, visto che ogni location è nominata con una lettera maiuscola. Per una mappa ‘random’ la dimensione massima di ‘size’ è 26 mentre per una mappa ‘square’ la dimensione massima di ‘size’ è 5. Con valori superiori l’applicazione genera errori.

#### Example
```json
{"init": "W", "goal": ["T", "A", "H", "C"], "size": 5, "world_type": "fixed", "solvers": ["DLFS", "IterativeSearch", "BFS", "BestFirstSearch"], "folder_path": "search/examples"}
```
### Mappa
Il file 'mappa.json' deve avere 3 valori all'interno:
- 'vertici': una lista di stringhe che rappresentano le location
- 'archi': una lista di tuple dove ogni tupla rappresenta un collegamento fra i due vertici specificati
- 'costi': una lista di interi. I costi devono corrispondere posizionalmente agli archi, quindi il primo costo della lista di interi sarà il costo del primo arco della lista degli archi, e così via

#### Example
```json
{
    "archi":[["W", "E"],["W", "A"], ["W", "B"], ["W", "C"], ["A", "Q"], ["A", "R"], ["A", "F"], ["A", "B"], ["B", "J"], ["B", "H"], ["B", "G"], ["C", "K"], ["C", "J"], ["D", "E"], ["D", "K"], ["E", "N"], ["E", "Q"], ["E", "P"], ["F", "G"], ["G", "S"], ["G", "H"], ["H", "T"], ["H", "I"], ["H", "J"], ["I", "U"], ["J", "V"], ["K", "N"], ["K", "L"], ["K", "V"], ["L", "M"], ["L", "N"], ["M", "O"], ["O", "P"], ["P", "Q"], ["Q", "R"], ["R", "S"], ["S", "T"], ["T", "U"], ["U", "V"]],
    "vertici": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"],
    "costi": [10, 11, 21, 18, 9, 10, 21, 3, 7, 6, 15, 13, 6, 8, 8, 9, 17, 16, 4, 22, 29, 34, 4, 7, 16, 6, 5, 17, 25, 31, 9, 10, 8, 13, 8, 6, 5, 7, 8]
}
```

### Salvataggio dei risultati
L'applicazione salva nella cartella specificata una cartella contenente la data e l'ora in cui è stata eseguita l'applicazione. All'interno di questa cartella saranno presenti:
- una rappresentazione grafica della mappa su cui si è effettuata la ricerca, 'mappa.svg'
- una rappresentazione grafica della soluzione, una per ogni algoritmo specificato, intesa come sottografo con le località visitate
- un file testuale di resoconto con informazioni sulla soluzione e sulle performance, 'results.txt'

## Trasformazione da JSON a problem.pddl
Per poter condurre dei test di confronto fra algoritmi di search e pddl è stata sviluppata questa classe di utility, che dato un file JSON della mappa e un file JSON di configurazione crea il relativo problem.pddl associato al dominio.

Per ottenere il file problem.pddl eseguire il file 'json-to-pddl-prob.py' specificando all'interno del codice le informazioni di interesse.

Nelle variabili globali
- PATH: è il percorso in cui verrà salvato il file, specificare prima il percorso e terminare con il nome del file e l'estensione .pddl
- MAPPA: è il percorso del file JSON rappresentante la mappa, da trasformare in rappresentazione pddl
- CONFIG: è il percorso del file JSON di configurazione, da questo file vengono lette le informazioni sullo stato iniziale e sul goal

### PDDL
- Scarica il solver ENHSP-20 --> https://sites.google.com/view/enhsp/ 
- Da riga di comando recati nella directory contente i file e usa il comando: Java -jar enhsp-20.jar -o domain.pddl -f problem.pddl -planner opt-hrmax
- Sostituisci "domain" e "problem" con i nomi che hai dato ai file
