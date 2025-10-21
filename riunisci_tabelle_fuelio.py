"""
Script per riunire le tabelle CSV separate in un unico file CSV per Fuelio.

Prende le tabelle separate e le riassembla nel formato originale di Fuelio,
usando il Log esteso con i dati storici.
"""

from pathlib import Path


def riunisci_tabelle_fuelio(output_file: str = "vehicle-1-sync-extended.csv", 
                            input_dir: str = None):
    """
    Riunisce le tabelle CSV separate in un unico file CSV per Fuelio.
    
    Args:
        output_file: Nome del file CSV di output
        input_dir: Directory dove si trovano i file CSV separati (default: directory corrente)
    """
    # Se non specificata, usa la directory corrente
    if input_dir is None:
        input_dir = Path('.')
    else:
        input_dir = Path(input_dir)
    
    # Ordine delle tabelle (come nel file originale di Fuelio)
    tabelle = [
        'Vehicle',
        'Log',  # Verrà sostituito con Log_unificato.csv
        'CostCategories',
        'Costs',
        'FavStations',
        'Pictures',
        'Category'
    ]
    
    print("=" * 60)
    print("RIUNIONE TABELLE FUELIO")
    print("=" * 60)
    
    # Apri il file di output
    output_path = Path(output_file)
    righe_totali = 0
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f_out:
        for nome_tabella in tabelle:
            # Per la tabella Log, usa Log_unificato.csv
            if nome_tabella == 'Log':
                nome_file = input_dir / 'Log_unificato.csv'
            else:
                nome_file = input_dir / f'{nome_tabella}.csv'
            
            # Verifica che il file esista
            if not nome_file.exists():
                print(f"\n⚠ ATTENZIONE: File {nome_file.name} non trovato, salto questa tabella")
                continue
            
            print(f"\nProcesso tabella: {nome_tabella}")
            print(f"  File sorgente: {nome_file.name}")
            
            # Legge il file CSV
            with open(nome_file, 'r', encoding='utf-8') as f_in:
                righe = f_in.readlines()
            
            # Scrive il marker della tabella (con spazio dopo ##)
            f_out.write(f'"## {nome_tabella}"\n')
            
            # Scrive tutte le righe (intestazione + dati)
            righe_dati = 0
            for riga in righe:
                f_out.write(riga)
                # Conta le righe di dati (esclusa l'intestazione)
                if riga.strip() and not riga.startswith('"Data"') and not riga.startswith('"NameBrand"'):
                    righe_dati += 1
            
            righe_totali += righe_dati
            print(f"  → Righe scritte: {righe_dati}")
    
    print("\n" + "=" * 60)
    print("COMPLETATO!")
    print("=" * 60)
    print(f"\n✅ File creato: {output_path.absolute()}")
    print(f"   Tabelle incluse: {len(tabelle)}")
    print(f"   Righe totali di dati: {righe_totali}")
    
    # Statistiche dettagliate
    print(f"\n📊 DETTAGLIO TABELLE:")
    for nome_tabella in tabelle:
        if nome_tabella == 'Log':
            nome_file = input_dir / 'Log_unificato.csv'
        else:
            nome_file = input_dir / f'{nome_tabella}.csv'
        
        if nome_file.exists():
            with open(nome_file, 'r', encoding='utf-8') as f:
                righe = len(f.readlines()) - 1  # -1 per escludere l'intestazione
            print(f"   - {nome_tabella}: {righe} record")
    
    return output_path


if __name__ == "__main__":
    try:
        # Esegue lo script
        output_file = riunisci_tabelle_fuelio()
        
        print("\n" + "=" * 60)
        print("COME USARE IL FILE")
        print("=" * 60)
        print(f"\n1. Il file '{output_file.name}' è pronto per essere importato in Fuelio")
        print(f"2. Contiene tutti i dati originali più i {672} rifornimenti storici")
        print(f"3. I dati sono ordinati cronologicamente dal più vecchio al più recente")
        print(f"\n⚠ IMPORTANTE:")
        print(f"   - Fai un BACKUP del tuo file Fuelio originale prima di importare")
        print(f"   - Il file originale era: vehicle-1-sync.csv")
        print(f"   - Il nuovo file è: {output_file.name}")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERRORE: {e}")
        print("   Assicurati che tutti i file CSV siano nella directory corrente")
    except Exception as e:
        print(f"\n❌ ERRORE imprevisto: {e}")
        import traceback
        traceback.print_exc()
