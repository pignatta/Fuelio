"""
Script per separare le tabelle del file CSV di Fuelio in file CSV individuali.

Il file CSV di Fuelio contiene più tabelle separate dal marker '##'.
Questo script identifica ogni tabella e crea un file CSV separato per ognuna.
"""

import csv
from pathlib import Path


def separa_tabelle_fuelio(file_path: str = "vehicle-1-sync.csv", output_dir: str = None):
    """
    Separa le tabelle del file CSV di Fuelio in file CSV individuali.
    
    Args:
        file_path: Percorso del file CSV originale
        output_dir: Directory dove salvare i file separati (default: stessa directory del file originale)
    """
    # Converte in Path object
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File non trovato: {file_path}")
    
    # Se non specificata, usa la stessa directory del file originale
    if output_dir is None:
        output_dir = file_path.parent
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # Legge il file e identifica le tabelle
    with open(file_path, 'r', encoding='utf-8') as f:
        righe = f.readlines()
    
    # Variabili per tracciare lo stato
    tabella_corrente = None
    intestazione_corrente = None
    righe_tabella = []
    tabelle_trovate = []
    
    print(f"Analisi del file: {file_path}")
    print("-" * 50)
    
    for i, riga in enumerate(righe):
        # Rimuove spazi bianchi iniziali/finali
        riga = riga.strip()
        
        # Controlla se è l'inizio di una nuova tabella
        if riga.startswith('"##') and riga.endswith('"'):
            # Salva la tabella precedente se esiste
            if tabella_corrente and intestazione_corrente:
                salva_tabella(tabella_corrente, intestazione_corrente, righe_tabella, output_dir)
                tabelle_trovate.append(tabella_corrente)
            
            # Estrae il nome della tabella (rimuove "## e ")
            tabella_corrente = riga.replace('"##', '').replace('"', '').strip()
            intestazione_corrente = None
            righe_tabella = []
            
            print(f"Trovata tabella: {tabella_corrente} (riga {i + 1})")
        
        elif tabella_corrente:
            # Se non abbiamo ancora l'intestazione, questa è l'intestazione
            if intestazione_corrente is None:
                intestazione_corrente = riga
            else:
                # Aggiungi la riga ai dati della tabella (solo se non vuota)
                if riga:
                    righe_tabella.append(riga)
    
    # Salva l'ultima tabella
    if tabella_corrente and intestazione_corrente:
        salva_tabella(tabella_corrente, intestazione_corrente, righe_tabella, output_dir)
        tabelle_trovate.append(tabella_corrente)
    
    print("-" * 50)
    print(f"\nProcesso completato!")
    print(f"Tabelle estratte: {len(tabelle_trovate)}")
    for nome in tabelle_trovate:
        print(f"  - {nome}.csv")
    print(f"\nFile salvati in: {output_dir.absolute()}")


def salva_tabella(nome_tabella: str, intestazione: str, righe: list, output_dir: Path):
    """
    Salva una tabella in un file CSV.
    
    Args:
        nome_tabella: Nome della tabella (sarà usato come nome file)
        intestazione: Intestazione della tabella
        righe: Lista di righe della tabella
        output_dir: Directory di output
    """
    # Crea il nome del file
    nome_file = output_dir / f"{nome_tabella}.csv"
    
    # Scrive il file CSV
    with open(nome_file, 'w', encoding='utf-8', newline='') as f:
        # Scrive intestazione
        f.write(intestazione + '\n')
        # Scrive le righe
        for riga in righe:
            f.write(riga + '\n')
    
    print(f"  → Salvata: {nome_file.name} ({len(righe)} righe)")


if __name__ == "__main__":
    try:
        # Esegue lo script
        separa_tabelle_fuelio()
    except FileNotFoundError as e:
        print(f"ERRORE: {e}")
        print("Assicurati che il file 'vehicle-1-sync.csv' sia nella stessa directory dello script.")
    except Exception as e:
        print(f"ERRORE imprevisto: {e}")
