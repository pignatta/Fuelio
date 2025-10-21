# Unione Log Storico con Log Fuelio

## Descrizione
Questo script unisce i dati storici dei rifornimenti dal file Excel con il registro Log di Fuelio, creando un unico file CSV ordinato cronologicamente.

## File richiesti
- `Contabilita_consumi_Punto.xlsx` - File Excel con i dati storici
- `Log.csv` - File Log esportato da Fuelio
- `Tabella_Conversione_Distro.xlsx` - Tabella di conversione distributori (opzionale)

## Mappatura delle colonne

### Dal file Excel al Log di Fuelio

| Colonna Excel | Colonna Log | Note |
|--------------|-------------|------|
| Data | Data | Convertita in formato `YYYY-MM-DD HH:MM` (ore fissate alle 12:00) |
| Km | Odo (km) | Mappatura diretta |
| Kg | kg | Mappatura diretta |
| Tot | Price (optional) | Mappatura diretta |
| €/Kg | VolumePrice | Mappatura diretta |
| A benzina | ExcludeDistance | Valori NaN convertiti in 0 |
| Serbatoio | TankNumber | Mappatura diretta |

### Campi calcolati

| Campo | Regola |
|-------|--------|
| Full | 1 se Serbatoio = 1 (metano), altrimenti 0 |
| FuelType | 501 se Serbatoio = 1 (metano), 110 se Serbatoio = 2 (GPL/Benzina) |
| UniqueId | Ricostruito in ordine cronologico crescente (dal più vecchio al più recente) |

### Campi vuoti/predefiniti
I seguenti campi sono impostati a valori predefiniti perché non presenti nei dati storici:
- `km/l (optional)` = vuoto
- `latitude (optional)` = NaN (nullo, popolato solo se distributore trovato)
- `longitude (optional)` = NaN (nullo, popolato solo se distributore trovato)
- `City (optional)` = vuoto (popolato solo se distributore trovato)
- `Notes (optional)` = vuoto
- `Missed` = 0
- `StationID (optional)` = NaN (nullo, popolato solo se distributore trovato)
- `TankCalc` = 0.0
- `Weather` = vuoto

### Formattazione numerica
Le colonne numeriche vengono formattate per compatibilità con Fuelio:
- **`kg`** - Arrotondata a 2 decimali
- **`Price (optional)`** - Arrotondata a 2 decimali  
- **`VolumePrice`** - Arrotondata a 2 decimali
- **`StationID (optional)`** - Convertita a intero (niente `.0`)

## Come usare lo script

### Opzione 1: Da Python
```python
python unisci_log_storico.py
```

### Opzione 2: Dal notebook Jupyter
Esegui la cella 17 del notebook `unione vecchi consumi.ipynb`:
```python
%run unisci_log_storico.py
```

## Output
Lo script crea un nuovo file `Log_unificato.csv` contenente:
- Tutti i record storici dal file Excel
- Tutti i record dal Log di Fuelio
- Record ordinati cronologicamente
- UniqueId progressivi dal più vecchio al più recente

## Note importanti

### Info sui distributori

#### Tabella di Conversione Distributori

Lo script utilizza la tabella `Tabella_Conversione_Distro.xlsx` per popolare i campi relativi ai distributori.

**Colonne richieste nella tabella di conversione:**
- `Conversione` - Nome del distributore usato nel file Excel (colonna "Distro")
- `StationID` - ID del distributore in Fuelio
- `NameBrand` - Nome/brand del distributore (opzionale, usato per costruire City)
- `Description` - Descrizione del distributore (opzionale, usato per costruire City)
- `Latitude` - Latitudine del distributore (opzionale)
- `Longitude` - Longitudine del distributore (opzionale)

**Nota:** La colonna `City` nel Log viene costruita automaticamente come `"NameBrand - Description"`

**Logica di applicazione:**

1. **Per i dati STORICI** (da `Contabilita_consumi_Punto.xlsx`):
   - Usa la colonna `Distro` del file Excel
   - Cerca il match nella colonna `Conversione` della tabella
   - Popola i campi `City`, `latitude`, `longitude`, `StationID`

2. **Per i dati NUOVI** (da `Log.csv` di Fuelio):
   - Usa la colonna `StationID (optional)` esistente
   - Cerca il match nella colonna `StationID` della tabella
   - Costruisce `City` come `"NameBrand - Description"`
   - Aggiorna i campi `latitude`, `longitude`

3. **Se il distributore non è presente** nella tabella:
   - `City` rimane vuoto
   - `latitude`, `longitude`, `StationID` rimangono `NaN` (nulli)
   - Nessun errore viene generato

### Tipo di carburante
Il campo `FuelType` viene determinato automaticamente in base al serbatoio:
- Serbatoio 1 → FuelType 501 (Metano)
- Serbatoio 2 → FuelType 110 (GPL/Benzina)

### Rifornimenti completi
Il campo `Full` indica se il rifornimento è stato completo:
- Full = 1 per il serbatoio del metano (Serbatoio 1)
- Full = 0 per gli altri carburanti

## Verifica del risultato
Dopo l'esecuzione, lo script mostra:
- Numero totale di record
- Periodo coperto (data min/max)
- Chilometraggio (km min/max)

Verifica che i dati siano corretti controllando il file `Log_unificato.csv`.
