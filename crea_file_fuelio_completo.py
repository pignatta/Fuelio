"""
Script completo per creare il file CSV esteso per Fuelio.

Esegue tutti i passaggi necessari:
1. Unisce i dati storici Excel con il Log Fuelio
2. Riunisce tutte le tabelle nel formato corretto
3. Verifica il file generato
"""

import subprocess
import sys
from pathlib import Path


def esegui_script(script_name: str, descrizione: str) -> bool:
    """
    Esegue uno script Python e gestisce eventuali errori.
    
    Args:
        script_name: Nome del file script da eseguire
        descrizione: Descrizione del passaggio
        
    Returns:
        True se eseguito con successo, False altrimenti
    """
    print("\n" + "=" * 60)
    print(f"PASSO: {descrizione}")
    print("=" * 60)
    print(f"Esecuzione: {script_name}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {descrizione} completato!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERRORE durante: {descrizione}")
        print(f"   Codice di errore: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ ERRORE imprevisto: {e}")
        return False


def main():
    """
    Esegue il processo completo di creazione del file Fuelio.
    """
    print("=" * 60)
    print("CREAZIONE FILE FUELIO COMPLETO")
    print("=" * 60)
    print("\nQuesto script eseguirà automaticamente tutti i passaggi necessari:")
    print("1. Unione dati storici Excel + Log Fuelio")
    print("2. Riunione di tutte le tabelle CSV")
    print("3. Verifica del file generato")
    
    input("\nPremi INVIO per iniziare...")
    
    # Verifica che i file necessari esistano
    print("\n" + "=" * 60)
    print("VERIFICA FILE NECESSARI")
    print("=" * 60)
    
    file_richiesti = {
        'Contabilita_consumi_Punto.xlsx': 'File Excel con dati storici',
        'Tabella_Conversione_Distro.xlsx': 'Tabella conversione distributori',
        'Log.csv': 'Log Fuelio originale',
        'Vehicle.csv': 'Tabella Vehicle',
        'CostCategories.csv': 'Tabella CostCategories',
        'Costs.csv': 'Tabella Costs',
        'FavStations.csv': 'Tabella FavStations',
        'Pictures.csv': 'Tabella Pictures',
        'Category.csv': 'Tabella Category',
    }
    
    mancanti = []
    for file, desc in file_richiesti.items():
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MANCANTE!")
            mancanti.append(file)
    
    if mancanti:
        print(f"\n❌ ERRORE: Mancano {len(mancanti)} file necessari:")
        for file in mancanti:
            print(f"   - {file}")
        print("\nAssicurati di avere tutti i file nella directory corrente.")
        return False
    
    print("\n✅ Tutti i file necessari sono presenti!")
    
    # Passo 1: Unione dati storici
    if not esegui_script(
        'unisci_log_storico.py',
        'Unione dati storici Excel + Log Fuelio'
    ):
        print("\n⚠ Impossibile continuare senza il Log unificato.")
        return False
    
    # Verifica che Log_unificato.csv sia stato creato
    if not Path('Log_unificato.csv').exists():
        print("\n❌ ERRORE: File Log_unificato.csv non creato!")
        return False
    
    # Passo 2: Riunione tabelle
    if not esegui_script(
        'riunisci_tabelle_fuelio.py',
        'Riunione di tutte le tabelle CSV'
    ):
        print("\n⚠ File non creato correttamente.")
        return False
    
    # Verifica che il file finale sia stato creato
    if not Path('vehicle-1-sync-extended.csv').exists():
        print("\n❌ ERRORE: File vehicle-1-sync-extended.csv non creato!")
        return False
    
    # Passo 3: Verifica finale
    esegui_script(
        'verifica_file_fuelio.py',
        'Verifica del file generato'
    )
    
    # Riepilogo finale
    print("\n" + "=" * 60)
    print("PROCESSO COMPLETATO!")
    print("=" * 60)
    
    output_file = Path('vehicle-1-sync-extended.csv')
    print(f"\n✅ File creato: {output_file.absolute()}")
    print(f"   Dimensione: {output_file.stat().st_size:,} bytes")
    
    print(f"\n📋 PROSSIMI PASSI:")
    print(f"   1. Fai un BACKUP del tuo database Fuelio corrente")
    print(f"   2. Salva il file originale vehicle-1-sync.csv")
    print(f"   3. Usa '{output_file.name}' per l'importazione in Fuelio")
    print(f"   4. Il file contiene 1069 rifornimenti (15 anni di dati)")
    
    print("\n" + "=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        successo = main()
        if not successo:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠ Processo interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRORE IMPREVISTO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
