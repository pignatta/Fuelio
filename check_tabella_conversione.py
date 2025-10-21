import pandas as pd

print("=" * 60)
print("VERIFICA TABELLA CONVERSIONE DISTRIBUTORI")
print("=" * 60)

try:
    df = pd.read_excel('Tabella_Conversione_Distro.xlsx')
    
    print(f"\n✅ File caricato con successo!")
    print(f"   Righe: {len(df)}")
    print(f"   Colonne: {len(df.columns)}")
    
    print("\n" + "=" * 60)
    print("COLONNE PRESENTI")
    print("=" * 60)
    for col in df.columns:
        print(f"  - {col}")
    
    # Verifica colonne obbligatorie
    print("\n" + "=" * 60)
    print("VERIFICA COLONNE OBBLIGATORIE")
    print("=" * 60)
    
    colonne_obbligatorie = ['Conversione', 'StationID']
    for col in colonne_obbligatorie:
        if col in df.columns:
            print(f"  ✅ {col} - presente")
        else:
            print(f"  ❌ {col} - MANCANTE!")
    
    # Verifica colonne opzionali
    print("\n" + "=" * 60)
    print("COLONNE OPZIONALI")
    print("=" * 60)
    
    colonne_opzionali = ['NameBrand', 'Description', 'Latitude', 'Longitude', 'CountryCode']
    for col in colonne_opzionali:
        if col in df.columns:
            valori_non_nulli = df[col].notna().sum()
            print(f"  ✅ {col} - presente ({valori_non_nulli}/{len(df)} valori)")
        else:
            print(f"  ⚠ {col} - non presente")
    
    # Verifica duplicati
    print("\n" + "=" * 60)
    print("VERIFICA DUPLICATI")
    print("=" * 60)
    
    if 'Conversione' in df.columns:
        duplicati_conv = df['Conversione'].duplicated().sum()
        if duplicati_conv > 0:
            print(f"  ❌ Trovati {duplicati_conv} duplicati nella colonna 'Conversione'!")
            print(f"     Valori duplicati: {df[df['Conversione'].duplicated()]['Conversione'].tolist()}")
        else:
            print(f"  ✅ Nessun duplicato nella colonna 'Conversione'")
    
    if 'StationID' in df.columns:
        duplicati_station = df['StationID'].duplicated().sum()
        if duplicati_station > 0:
            print(f"  ❌ Trovati {duplicati_station} duplicati nella colonna 'StationID'!")
            print(f"     Valori duplicati: {df[df['StationID'].duplicated()]['StationID'].tolist()}")
        else:
            print(f"  ✅ Nessun duplicato nella colonna 'StationID'")
    
    # Verifica valori nulli
    print("\n" + "=" * 60)
    print("VALORI NULLI NELLE COLONNE OBBLIGATORIE")
    print("=" * 60)
    
    if 'Conversione' in df.columns:
        nulli_conv = df['Conversione'].isna().sum()
        if nulli_conv > 0:
            print(f"  ⚠ Conversione: {nulli_conv} valori nulli")
        else:
            print(f"  ✅ Conversione: nessun valore nullo")
    
    if 'StationID' in df.columns:
        nulli_station = df['StationID'].isna().sum()
        if nulli_station > 0:
            print(f"  ⚠ StationID: {nulli_station} valori nulli")
        else:
            print(f"  ✅ StationID: nessun valore nullo")
    
    # Verifica NameBrand e Description per costruzione City
    print("\n" + "=" * 60)
    print("VERIFICA COSTRUZIONE CITY")
    print("=" * 60)
    
    if 'NameBrand' in df.columns and 'Description' in df.columns:
        # Conta quante righe hanno entrambi i campi vuoti
        entrambi_vuoti = ((df['NameBrand'].isna() | (df['NameBrand'] == '')) & 
                         (df['Description'].isna() | (df['Description'] == ''))).sum()
        
        if entrambi_vuoti > 0:
            print(f"  ⚠ {entrambi_vuoti} righe hanno sia NameBrand che Description vuoti")
            print(f"    → La colonna City risulterà vuota per questi distributori")
        else:
            print(f"  ✅ Tutte le righe hanno almeno NameBrand o Description")
        
        # Conta quante hanno entrambi
        entrambi_pieni = ((df['NameBrand'].notna() & (df['NameBrand'] != '')) & 
                         (df['Description'].notna() & (df['Description'] != ''))).sum()
        print(f"  → {entrambi_pieni}/{len(df)} righe hanno sia NameBrand che Description")
        print(f"    → City = 'NameBrand - Description'")
    else:
        print(f"  ⚠ NameBrand e/o Description non presenti nella tabella")
        print(f"    → La colonna City non verrà popolata correttamente")
    
    # Mostra prime righe
    print("\n" + "=" * 60)
    print("PRIME 10 RIGHE")
    print("=" * 60)
    print(df.head(10).to_string())
    
    print("\n" + "=" * 60)
    print("RIEPILOGO")
    print("=" * 60)
    print(f"Totale distributori: {len(df)}")
    if 'Conversione' in df.columns:
        print(f"Conversioni uniche: {df['Conversione'].nunique()}")
    if 'StationID' in df.columns:
        print(f"StationID univoci: {df['StationID'].nunique()}")
    
except FileNotFoundError:
    print("\n❌ ERRORE: File 'Tabella_Conversione_Distro.xlsx' non trovato!")
    print("   Assicurati che il file sia nella directory corrente.")
except Exception as e:
    print(f"\n❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()
