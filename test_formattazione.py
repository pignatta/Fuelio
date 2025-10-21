"""
Script di test per verificare la formattazione delle colonne nel Log unificato.

Controlla:
- kg, Price, VolumePrice arrotondati a 2 decimali
- StationID come intero senza .0
"""

import pandas as pd


def test_formattazione():
    """
    Verifica la formattazione delle colonne nel Log_unificato.csv
    """
    print("=" * 60)
    print("TEST FORMATTAZIONE COLONNE")
    print("=" * 60)
    
    try:
        df = pd.read_csv('Log_unificato.csv')
        
        print(f"\n✅ File caricato: {len(df)} righe")
        
        print("\n" + "=" * 60)
        print("VERIFICA FORMATTAZIONE")
        print("=" * 60)
        
        # Test 1: kg arrotondato a 2 decimali
        print("\n1. Colonna 'kg':")
        campioni_kg = df['kg'].head(10)
        for i, val in enumerate(campioni_kg):
            # Conta i decimali
            str_val = str(val)
            if '.' in str_val:
                decimali = len(str_val.split('.')[1])
                print(f"   Riga {i+1}: {val} → {decimali} decimali {'✅' if decimali <= 2 else '❌'}")
            else:
                print(f"   Riga {i+1}: {val} → intero ✅")
        
        # Test 2: Price (optional) arrotondato a 2 decimali
        print("\n2. Colonna 'Price (optional)':")
        campioni_price = df['Price (optional)'].head(10)
        for i, val in enumerate(campioni_price):
            if pd.notna(val):
                str_val = str(val)
                if '.' in str_val:
                    decimali = len(str_val.split('.')[1])
                    print(f"   Riga {i+1}: {val} → {decimali} decimali {'✅' if decimali <= 2 else '❌'}")
                else:
                    print(f"   Riga {i+1}: {val} → intero ✅")
        
        # Test 3: VolumePrice arrotondato a 2 decimali
        print("\n3. Colonna 'VolumePrice':")
        campioni_volume = df['VolumePrice'].head(10)
        for i, val in enumerate(campioni_volume):
            str_val = str(val)
            if '.' in str_val:
                decimali = len(str_val.split('.')[1])
                print(f"   Riga {i+1}: {val} → {decimali} decimali {'✅' if decimali <= 2 else '❌'}")
            else:
                print(f"   Riga {i+1}: {val} → intero ✅")
        
        # Test 4: StationID come intero (no .0)
        print("\n4. Colonna 'StationID (optional)':")
        campioni_station = df['StationID (optional)'].head(10)
        for i, val in enumerate(campioni_station):
            if pd.notna(val):
                str_val = str(val)
                ha_decimale = '.' in str_val
                print(f"   Riga {i+1}: {val} → {'❌ ha decimale!' if ha_decimale else '✅ intero'}")
            else:
                print(f"   Riga {i+1}: (vuoto) ✅")
        
        # Riepilogo statistico
        print("\n" + "=" * 60)
        print("STATISTICHE COMPLETE")
        print("=" * 60)
        
        # Verifica max decimali per kg
        max_dec_kg = df['kg'].apply(lambda x: len(str(x).split('.')[1]) if '.' in str(x) else 0).max()
        print(f"\nkg:")
        print(f"  Max decimali trovati: {max_dec_kg} {'✅' if max_dec_kg <= 2 else '❌'}")
        print(f"  Range: {df['kg'].min():.2f} - {df['kg'].max():.2f}")
        
        # Verifica max decimali per Price
        max_dec_price = df['Price (optional)'].apply(lambda x: len(str(x).split('.')[1]) if pd.notna(x) and '.' in str(x) else 0).max()
        print(f"\nPrice (optional):")
        print(f"  Max decimali trovati: {max_dec_price} {'✅' if max_dec_price <= 2 else '❌'}")
        print(f"  Range: {df['Price (optional)'].min():.2f} - {df['Price (optional)'].max():.2f}")
        
        # Verifica max decimali per VolumePrice
        max_dec_vol = df['VolumePrice'].apply(lambda x: len(str(x).split('.')[1]) if '.' in str(x) else 0).max()
        print(f"\nVolumePrice:")
        print(f"  Max decimali trovati: {max_dec_vol} {'✅' if max_dec_vol <= 2 else '❌'}")
        print(f"  Range: {df['VolumePrice'].min():.2f} - {df['VolumePrice'].max():.2f}")
        
        # Verifica StationID
        station_con_decimali = df['StationID (optional)'].apply(lambda x: '.' in str(x) if pd.notna(x) else False).sum()
        print(f"\nStationID (optional):")
        print(f"  Valori con decimali: {station_con_decimali} {'✅' if station_con_decimali == 0 else '❌'}")
        print(f"  Range: {df['StationID (optional)'].min():.0f} - {df['StationID (optional)'].max():.0f}")
        
        print("\n" + "=" * 60)
        
        # Risultato finale
        if max_dec_kg <= 2 and max_dec_price <= 2 and max_dec_vol <= 2 and station_con_decimali == 0:
            print("\n✅ TUTTO OK! Formattazione corretta.")
        else:
            print("\n❌ PROBLEMI RILEVATI! Controlla i dettagli sopra.")
        
        print("=" * 60)
        
    except FileNotFoundError:
        print("\n❌ ERRORE: File 'Log_unificato.csv' non trovato!")
        print("   Esegui prima 'python unisci_log_storico.py'")
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_formattazione()
