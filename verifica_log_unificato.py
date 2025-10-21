"""
Script per verificare il Log unificato creato.

Controlla:
- Presenza di NaN nei campi del distributore
- Statistiche sui distributori trovati/non trovati
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("VERIFICA LOG UNIFICATO")
print("=" * 60)

try:
    df = pd.read_csv('Log_unificato.csv')
    
    print(f"\n✅ File caricato con successo!")
    print(f"   Totale rifornimenti: {len(df)}")
    
    print("\n" + "=" * 60)
    print("STATISTICHE DISTRIBUTORI")
    print("=" * 60)
    
    # Conta rifornimenti con/senza distributore
    con_station = df['StationID (optional)'].notna().sum()
    senza_station = df['StationID (optional)'].isna().sum()
    
    print(f"\nStationID:")
    print(f"  ✅ Con distributore: {con_station} ({con_station/len(df)*100:.1f}%)")
    print(f"  ⚠ Senza distributore (NaN): {senza_station} ({senza_station/len(df)*100:.1f}%)")
    
    # Conta rifornimenti con/senza coordinate
    con_lat = df['latitude (optional)'].notna().sum()
    senza_lat = df['latitude (optional)'].isna().sum()
    
    print(f"\nCoordinate:")
    print(f"  ✅ Con coordinate: {con_lat} ({con_lat/len(df)*100:.1f}%)")
    print(f"  ⚠ Senza coordinate (NaN): {senza_lat} ({senza_lat/len(df)*100:.1f}%)")
    
    # Conta rifornimenti con/senza City
    con_city = (df['City (optional)'].notna() & (df['City (optional)'] != '')).sum()
    senza_city = (~df['City (optional)'].notna() | (df['City (optional)'] == '')).sum()
    
    print(f"\nCity:")
    print(f"  ✅ Con nome: {con_city} ({con_city/len(df)*100:.1f}%)")
    print(f"  ⚠ Senza nome: {senza_city} ({senza_city/len(df)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("PERIODO E CHILOMETRAGGIO")
    print("=" * 60)
    
    print(f"\nData:")
    print(f"  Primo rifornimento: {df['Data'].min()}")
    print(f"  Ultimo rifornimento: {df['Data'].max()}")
    
    print(f"\nChilometraggio:")
    print(f"  Iniziale: {df['Odo (km)'].min():.0f} km")
    print(f"  Finale: {df['Odo (km)'].max():.0f} km")
    print(f"  Totale percorso: {df['Odo (km)'].max() - df['Odo (km)'].min():.0f} km")
    
    print("\n" + "=" * 60)
    print("PRIMI RIFORNIMENTI SENZA DISTRIBUTORE")
    print("=" * 60)
    
    senza_distro = df[df['StationID (optional)'].isna()].head(5)
    if len(senza_distro) > 0:
        print(f"\nPrime {len(senza_distro)} righe senza distributore:")
        print(senza_distro[['Data', 'Odo (km)', 'kg', 'StationID (optional)', 
                           'latitude (optional)', 'longitude (optional)', 'City (optional)']].to_string())
    else:
        print("\n✅ Tutti i rifornimenti hanno un distributore associato!")
    
    print("\n" + "=" * 60)
    print("VERIFICA UNIQUEID")
    print("=" * 60)
    
    # Verifica UniqueId sia sequenziale
    expected_ids = list(range(1, len(df) + 1))
    actual_ids = df['UniqueId'].tolist()
    
    if expected_ids == actual_ids:
        print(f"  ✅ UniqueId sequenziali da 1 a {len(df)}")
    else:
        print(f"  ❌ UniqueId NON sequenziali!")
        # Trova i primi ID non corretti
        for i, (exp, act) in enumerate(zip(expected_ids[:10], actual_ids[:10])):
            if exp != act:
                print(f"     Posizione {i}: atteso {exp}, trovato {act}")
    
    print("\n" + "=" * 60)
    
except FileNotFoundError:
    print("\n❌ ERRORE: File 'Log_unificato.csv' non trovato!")
    print("   Esegui prima 'python unisci_log_storico.py'")
except Exception as e:
    print(f"\n❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()
