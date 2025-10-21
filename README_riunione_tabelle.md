# Riunione Tabelle Fuelio

Script per ricreare il file CSV completo di Fuelio con i dati storici integrati.

## 📋 Descrizione

Questo script prende le tabelle CSV separate e le riassembla nel formato originale di Fuelio (`vehicle-1-sync.csv`), sostituendo la tabella `Log` con `Log_unificato.csv` che contiene sia i dati storici che quelli recenti.

## 🔄 Processo

### 1. Separazione Iniziale
Il file originale `vehicle-1-sync.csv` è stato separato in:
- `Vehicle.csv` - Informazioni sul veicolo
- `Log.csv` - Log rifornimenti originale (397 record)
- `CostCategories.csv` - Categorie di costo
- `Costs.csv` - Costi
- `FavStations.csv` - Stazioni preferite
- `Pictures.csv` - Foto
- `Category.csv` - Categorie

### 2. Integrazione Dati Storici
I dati storici da Excel sono stati uniti con il Log di Fuelio creando:
- `Log_unificato.csv` - Log completo (1069 record = 672 storici + 397 recenti)

### 3. Riunione Finale
Tutte le tabelle vengono riunite in:
- `vehicle-1-sync-extended.csv` - File completo pronto per Fuelio

## 🚀 Come Usare

### Esecuzione
```bash
python riunisci_tabelle_fuelio.py
```

### Risultato
Viene creato il file `vehicle-1-sync-extended.csv` con:
- **Tutte le tabelle originali** (Vehicle, CostCategories, Costs, FavStations, Pictures, Category)
- **Log esteso** con 1069 rifornimenti (dal 2010 al 2025)

## 📊 Struttura del File Output

Il file `vehicle-1-sync-extended.csv` ha la seguente struttura:

```
"##Vehicle"
[intestazione]
[dati veicolo]

"##Log"
[intestazione]
[1069 rifornimenti ordinati cronologicamente]

"##CostCategories"
[intestazione]
[categorie di costo]

"##Costs"
[intestazione]
[costi]

"##FavStations"
[intestazione]
[stazioni preferite]

"##Pictures"
[intestazione]
[foto]

"##Category"
[intestazione]
[categorie]
```

## ⚠️ IMPORTANTE

### Prima di Importare in Fuelio

1. **Fai un BACKUP completo** del tuo database Fuelio corrente
2. **Testa l'importazione** su un veicolo di prova se possibile
3. **Verifica** che tutti i dati siano corretti nel file generato

### Ordine delle Tabelle

L'ordine delle tabelle nel file è **critico** e deve essere rispettato:
1. Vehicle
2. Log
3. CostCategories
4. Costs
5. FavStations
6. Pictures
7. Category

Lo script mantiene automaticamente questo ordine.

### Compatibilità

Il file generato è compatibile con Fuelio perché:
- ✅ Mantiene la struttura originale con i marker `##`
- ✅ Rispetta l'ordine delle tabelle
- ✅ Usa le stesse colonne e formati
- ✅ I campi opzionali vuoti sono gestiti correttamente (NaN → celle vuote)

## 📈 Statistiche

### Dati Storici Integrati
- **672 rifornimenti** dal file Excel (2010-2021)
- **397 rifornimenti** dal Log Fuelio originale (2021-2025)
- **Totale: 1069 rifornimenti**

### Periodo Coperto
- Dal: 2010-02-02
- Al: 2025-10-16
- **Durata: ~15 anni**

### Chilometraggio
- Iniziale: 1,732 km
- Finale: 313,901 km
- **Totale percorso: 312,169 km**

## 🔍 Verifica del File Generato

### Controllo Manuale
Puoi aprire il file `vehicle-1-sync-extended.csv` con un editor di testo per verificare:
1. Presenza di tutti i marker `##NomeTabella`
2. Ordine corretto delle tabelle
3. Numero di righe in ogni tabella

### Controllo Automatico
Usa lo script di verifica:
```bash
python verifica_log_unificato.py
```

## 📝 File Necessari

Lo script richiede che siano presenti nella stessa directory:
- [x] `Vehicle.csv`
- [x] `Log_unificato.csv` (creato da `unisci_log_storico.py`)
- [x] `CostCategories.csv`
- [x] `Costs.csv`
- [x] `FavStations.csv`
- [x] `Pictures.csv`
- [x] `Category.csv`

## 🛠️ Risoluzione Problemi

### Errore: File non trovato
**Causa**: Manca uno dei file CSV necessari

**Soluzione**: 
1. Verifica che tutti i file CSV siano nella directory
2. Se manca `Log_unificato.csv`, esegui prima `python unisci_log_storico.py`
3. Se mancano gli altri file, esegui prima `python separa_tabelle_fuelio.py`

### Errore: Encoding non corretto
**Causa**: Il file potrebbe avere un encoding diverso da UTF-8

**Soluzione**: Lo script usa UTF-8, che è lo standard per Fuelio

## 📚 Script Correlati

1. **`separa_tabelle_fuelio.py`** - Separa il file originale in tabelle CSV
2. **`unisci_log_storico.py`** - Unisce i dati storici con il Log Fuelio
3. **`riunisci_tabelle_fuelio.py`** - Riassembla tutte le tabelle (questo script)
4. **`verifica_log_unificato.py`** - Verifica il Log unificato

## 🎯 Workflow Completo

```
1. vehicle-1-sync.csv (originale)
   ↓ separa_tabelle_fuelio.py
2. Vehicle.csv, Log.csv, Costs.csv, ecc.
   ↓ 
3. Log.csv + Contabilita_consumi_Punto.xlsx
   ↓ unisci_log_storico.py
4. Log_unificato.csv (1069 record)
   ↓ riunisci_tabelle_fuelio.py
5. vehicle-1-sync-extended.csv (FINALE)
   ↓ 
6. Importa in Fuelio ✅
```

## ✅ Checklist Pre-Importazione

- [ ] Backup del database Fuelio effettuato
- [ ] File `vehicle-1-sync-extended.csv` generato
- [ ] Verifica visiva del file completata
- [ ] Numero di rifornimenti corretto (1069)
- [ ] Tutte le tabelle presenti nel file
- [ ] Pronto per l'importazione in Fuelio

---

**Data ultima modifica**: 21 Ottobre 2025
**Versione**: 1.0
