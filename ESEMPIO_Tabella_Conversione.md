# Struttura Tabella di Conversione Distributori

## Descrizione
Questo documento descrive la struttura richiesta per il file `Tabella_Conversione_Distro.xlsx`.

## Colonne Richieste

### Colonne Obbligatorie

| Colonna | Tipo | Descrizione | Esempio |
|---------|------|-------------|---------|
| `Conversione` | Testo | Nome del distributore usato nel file Excel vecchio (colonna "Distro") | `G`, `CdC`, `M`, `BALANZANO` |
| `StationID` | Numero | ID univoco del distributore in Fuelio | `464075`, `361768`, `89914` |

### Colonne Opzionali (ma consigliate)

| Colonna | Tipo | Descrizione | Esempio |
|---------|------|-------------|---------|
| `NameBrand` | Testo | Nome/brand del distributore (usato per costruire City) | `Metano Service`, `SEP`, `IP` |
| `Description` | Testo | Descrizione/località del distributore (usato per costruire City) | `Metano Service`, `Gubbio`, `IP` |
| `Latitude` | Decimale | Latitudine geografica | `43.36295` |
| `Longitude` | Decimale | Longitudine geografica | `12.54616` |
| `CountryCode` | Testo | Codice paese (ISO 3166-1 alpha-3) | `ITA` |

**Nota importante:** La colonna `City` nel Log viene costruita **automaticamente** come `"NameBrand - Description"`. Non è necessario inserirla nella tabella di conversione.

## Esempio di Struttura

```
| Conversione | StationID | NameBrand                  | Description                   | Latitude  | Longitude | CountryCode |
|-------------|-----------|----------------------------|-------------------------------|-----------|-----------|-------------|
| G           | 464075    | Metano Service             | Metano Service                | 43.36295  | 12.54616  | ITA         |
| SEP         | 361768    | SEP                        | Gubbio                        | 43.35304  | 12.56143  | ITA         |
| CdC         | 89914     | IP                         | IP                            | 43.12885  | 12.42243  | ITA         |
| BALANZANO   | 398401    | Stazione di Servizio IS    | Ponte S. Giovanni             | 43.07468  | 12.42811  | ITA         |
```

**Risultato nel Log:**
- Per `G` → City = `"Metano Service - Metano Service"`
- Per `SEP` → City = `"SEP - Gubbio"`
- Per `CdC` → City = `"IP - IP"`
- Per `BALANZANO` → City = `"Stazione di Servizio IS - Ponte S. Giovanni"`

## Come Funziona il Matching

### Per i Dati Storici
1. Lo script legge la colonna `Distro` dal file `Contabilita_consumi_Punto.xlsx`
2. Cerca il valore nella colonna `Conversione` della tabella
3. Se trova un match, copia tutte le informazioni del distributore nel Log

**Esempio:**
- Nel file Excel c'è un rifornimento con `Distro = "G"`
- Lo script cerca `"G"` nella colonna `Conversione`
- Trova il match e popola:
  - `StationID (optional)` = 464075
  - `City (optional)` = "Metano Service - Metano Service" (costruita da NameBrand + " - " + Description)
  - `latitude (optional)` = 43.36295
  - `longitude (optional)` = 12.54616

### Per i Dati Fuelio (Nuovi)
1. Lo script legge la colonna `StationID (optional)` dal file `Log.csv`
2. Cerca il valore nella colonna `StationID` della tabella
3. Se trova un match, AGGIORNA le informazioni del distributore (ad es. se hai cambiato nome)

**Esempio:**
- Nel Log.csv c'è un rifornimento con `StationID (optional) = 464075`
- Lo script cerca `464075` nella colonna `StationID`
- Trova il match e aggiorna:
  - `City (optional)` = "Metano Service - Metano Service" (costruita da NameBrand + " - " + Description)
  - `latitude (optional)` = 43.36295
  - `longitude (optional)` = 12.54616

## Note Importanti

### Costruzione del Campo City

La colonna `City` viene costruita secondo queste regole:

1. **Se sono presenti sia NameBrand che Description:**
   - City = `"NameBrand - Description"`
   - Esempio: `"Metano Service - Metano Service"`, `"SEP - Gubbio"`

2. **Se è presente solo NameBrand:**
   - City = `"NameBrand"`
   - Esempio: Se Description è vuoto e NameBrand è `"IP"`, allora City = `"IP"`

3. **Se è presente solo Description:**
   - City = `"Description"`
   - Esempio: Se NameBrand è vuoto e Description è `"Gubbio"`, allora City = `"Gubbio"`

4. **Se entrambi sono vuoti:**
   - City rimane vuoto

### Valori Mancanti
- Se un distributore NON è presente nella tabella di conversione:
  - `City` rimane vuoto
  - `latitude`, `longitude`, `StationID` rimangono `NaN` (nulli, non vengono impostati a 0)
  - NON viene generato alcun errore
  - Il rifornimento viene comunque incluso nel Log unificato

### Duplicati
- Assicurati che ogni valore nella colonna `Conversione` sia univoco
- Assicurati che ogni valore nella colonna `StationID` sia univoco
- In caso di duplicati, viene usato il primo match trovato

### Case Sensitivity
- Il matching è **case-sensitive** (distingue maiuscole/minuscole)
- `"G"` è diverso da `"g"`
- Assicurati che i valori corrispondano esattamente

## Come Creare la Tabella

### Opzione 1: Excel
1. Apri Excel
2. Crea un nuovo foglio
3. Inserisci le intestazioni nella prima riga
4. Compila i dati per ogni distributore
5. Salva come `Tabella_Conversione_Distro.xlsx`

### Opzione 2: Da Dati Esistenti
Se hai già i distributori in Fuelio (nel file FavStations.csv):
1. Apri `FavStations.csv`
2. Aggiungi una colonna `Conversione` all'inizio
3. Riempi manualmente i nomi storici dalla colonna `Distro` del vecchio Excel
4. Salva come `Tabella_Conversione_Distro.xlsx`

## Verifica della Tabella

Per verificare che la tabella sia corretta, puoi eseguire:
```python
python check_tabella_conversione.py
```

Questo script mostrerà:
- Le colonne presenti
- Il numero di righe
- Eventuali valori duplicati o mancanti
