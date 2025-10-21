"""
Script per verificare la correttezza del file CSV riassemblato per Fuelio.

Controlla:
- Presenza e ordine delle tabelle
- Struttura del file
- Numero di record per tabella
"""

from pathlib import Path


def verifica_file_fuelio(file_path: str = "vehicle-1-sync-extended.csv"):
    """
    Verifica la correttezza del file CSV per Fuelio.
    
    Args:
        file_path: Percorso del file da verificare
    """
    print("=" * 60)
    print("VERIFICA FILE FUELIO")
    print("=" * 60)
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"\n❌ ERRORE: File '{file_path}' non trovato!")
        return False
    
    print(f"\n✅ File trovato: {file_path.name}")
    print(f"   Dimensione: {file_path.stat().st_size:,} bytes")
    
    # Legge il file
    with open(file_path, 'r', encoding='utf-8') as f:
        righe = f.readlines()
    
    print(f"   Righe totali: {len(righe):,}")
    
    # Tabelle attese nell'ordine corretto
    tabelle_attese = [
        'Vehicle',
        'Log',
        'CostCategories',
        'Costs',
        'FavStations',
        'Pictures',
        'Category'
    ]
    
    # Analizza la struttura del file
    print("\n" + "=" * 60)
    print("STRUTTURA FILE")
    print("=" * 60)
    
    tabelle_trovate = []
    tabella_corrente = None
    righe_per_tabella = {}
    
    for i, riga in enumerate(righe):
        riga_stripped = riga.strip()
        
        # Controlla se è un marker di tabella (formato: "## NomeTabella")
        if riga_stripped.startswith('"##') and riga_stripped.endswith('"'):
            # Salva il conteggio della tabella precedente
            if tabella_corrente:
                righe_per_tabella[tabella_corrente] = righe_per_tabella.get(tabella_corrente, 0)
            
            # Estrae il nome della tabella (rimuove "## e le virgolette)
            nome_tabella = riga_stripped.replace('"## ', '').replace('"##', '').replace('"', '').strip()
            tabelle_trovate.append(nome_tabella)
            tabella_corrente = nome_tabella
            righe_per_tabella[nome_tabella] = -1  # -1 perché escludiamo l'intestazione
        
        elif tabella_corrente and riga_stripped:
            # Conta le righe di questa tabella
            righe_per_tabella[tabella_corrente] = righe_per_tabella.get(tabella_corrente, -1) + 1
    
    # Verifica ordine e presenza delle tabelle
    print("\nTabelle trovate:")
    
    tutto_ok = True
    for i, tabella_attesa in enumerate(tabelle_attese):
        if i < len(tabelle_trovate):
            tabella_trovata = tabelle_trovate[i]
            record = righe_per_tabella.get(tabella_trovata, 0)
            
            if tabella_trovata == tabella_attesa:
                print(f"  {i+1}. ✅ {tabella_trovata} ({record} record)")
            else:
                print(f"  {i+1}. ❌ Trovata '{tabella_trovata}' invece di '{tabella_attesa}' ({record} record)")
                tutto_ok = False
        else:
            print(f"  {i+1}. ❌ {tabella_attesa} - MANCANTE!")
            tutto_ok = False
    
    # Tabelle extra non previste
    if len(tabelle_trovate) > len(tabelle_attese):
        print(f"\n⚠ Trovate {len(tabelle_trovate) - len(tabelle_attese)} tabelle extra:")
        for tabella in tabelle_trovate[len(tabelle_attese):]:
            print(f"  - {tabella}")
    
    # Verifica specifiche per la tabella Log
    print("\n" + "=" * 60)
    print("VERIFICA TABELLA LOG")
    print("=" * 60)
    
    if 'Log' in righe_per_tabella:
        record_log = righe_per_tabella['Log']
        print(f"\nRecord nel Log: {record_log}")
        
        if record_log == 1069:
            print(f"  ✅ Numero corretto! (672 storici + 397 recenti)")
        elif record_log == 397:
            print(f"  ⚠ ATTENZIONE: Sembra il Log originale, non quello esteso!")
            print(f"     Assicurati di aver usato Log_unificato.csv")
            tutto_ok = False
        elif record_log == 672:
            print(f"  ⚠ ATTENZIONE: Sembra contenere solo i dati storici!")
            tutto_ok = False
        else:
            print(f"  ⚠ Numero inaspettato di record")
    else:
        print("\n❌ Tabella Log non trovata!")
        tutto_ok = False
    
    # Riepilogo finale
    print("\n" + "=" * 60)
    print("RIEPILOGO")
    print("=" * 60)
    
    if tutto_ok:
        print("\n✅ TUTTO OK!")
        print(f"   Il file '{file_path.name}' è pronto per essere importato in Fuelio")
        print(f"\n   Statistiche:")
        print(f"   - Tabelle: {len(tabelle_trovate)}/{len(tabelle_attese)}")
        print(f"   - Record totali: {sum(righe_per_tabella.values()):,}")
        print(f"   - Record nel Log: {righe_per_tabella.get('Log', 0):,}")
        
        print(f"\n   ⚠ RICORDA:")
        print(f"   - Fai un BACKUP del tuo database Fuelio prima di importare")
        print(f"   - Il file contiene {righe_per_tabella.get('Log', 0)} rifornimenti (15 anni di dati)")
    else:
        print("\n❌ PROBLEMI RILEVATI!")
        print(f"   Controlla i messaggi sopra per i dettagli")
        print(f"   Potrebbe essere necessario rigenerare il file")
    
    print("\n" + "=" * 60)
    
    return tutto_ok


if __name__ == "__main__":
    try:
        # Verifica il file
        verifica_file_fuelio()
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
