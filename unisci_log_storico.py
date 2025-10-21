"""
Script per unire i dati storici dal file Excel con il registro Log di Fuelio.

Legge i dati dal file Excel "Contabilita_consumi_Punto.xlsx" e li unisce
al file Log.csv di Fuelio, ricostruendo la colonna UniqueId in ordine cronologico.
"""

import pandas as pd
import numpy as np
import csv
from datetime import datetime, timedelta
from pathlib import Path


def carica_dati_excel(file_excel: str = "Contabilita_consumi_Punto.xlsx") -> pd.DataFrame:
    """
    Carica i dati storici dal file Excel.
    
    Args:
        file_excel: Percorso del file Excel
        
    Returns:
        DataFrame con i dati storici
    """
    print(f"Caricamento dati da {file_excel}...")
    
    # Legge il file Excel con header alla riga 2 (indice 2, quindi terza riga)
    df = pd.read_excel(file_excel, header=[2])
    
    print(f"  → Caricati {len(df)} record storici")
    print(f"  → Colonne: {df.columns.tolist()}")
    
    return df


def carica_tabella_conversione(file_conversione: str = "Tabella_Conversione_Distro.xlsx") -> pd.DataFrame:
    """
    Carica la tabella di conversione distributori.
    
    Args:
        file_conversione: Percorso del file di conversione
        
    Returns:
        DataFrame con la tabella di conversione
    """
    print(f"\nCaricamento tabella conversione da {file_conversione}...")
    
    df = pd.read_excel(file_conversione)
    
    print(f"  → Caricati {len(df)} distributori")
    print(f"  → Colonne: {df.columns.tolist()}")
    
    return df


def carica_log_fuelio(file_log: str = "Log.csv") -> pd.DataFrame:
    """
    Carica il file Log.csv di Fuelio.
    
    Args:
        file_log: Percorso del file Log.csv
        
    Returns:
        DataFrame con i dati di Fuelio
    """
    print(f"\nCaricamento dati da {file_log}...")
    
    df = pd.read_csv(file_log)
    
    print(f"  → Caricati {len(df)} record da Fuelio")
    
    return df


def converti_dati_excel(df_excel: pd.DataFrame, df_conversione: pd.DataFrame = None) -> pd.DataFrame:
    """
    Converte i dati dal formato Excel al formato Log di Fuelio.
    
    Args:
        df_excel: DataFrame con i dati Excel
        df_conversione: DataFrame con la tabella di conversione distributori (opzionale)
        
    Returns:
        DataFrame convertito nel formato Log
    """
    print("\nConversione dati Excel al formato Fuelio...")
    
    # Crea un nuovo DataFrame con le colonne del Log
    df_convertito = pd.DataFrame()
    
    # Conversione Data: aggiungi 12:00 come ora
    df_convertito['Data'] = pd.to_datetime(df_excel['Data'])
    df_convertito['Data'] = df_convertito['Data'] + timedelta(hours=12)
    df_convertito['Data'] = df_convertito['Data'].dt.strftime('%Y-%m-%d %H:%M')
    
    # Mappatura diretta delle colonne
    df_convertito['Odo (km)'] = df_excel['Km']
    df_convertito['kg'] = df_excel['Kg']
    df_convertito['Price (optional)'] = df_excel['Tot']
    df_convertito['VolumePrice'] = df_excel['€/Kg']
    df_convertito['TankNumber'] = df_excel['Serbatoio']
    
    # Gestione ExcludeDistance: converte NaN in 0
    df_convertito['ExcludeDistance'] = df_excel.get('A benzina', 0)
    df_convertito['ExcludeDistance'] = df_convertito['ExcludeDistance'].fillna(0)
    
    # Gestione Full: 1 se Serbatoio==1 (metano), 0 altrimenti
    df_convertito['Full'] = (df_excel['Serbatoio'] == 1).astype(int)
    
    # Gestione FuelType in base al serbatoio
    # Serbatoio 1 = Metano (FuelType 501), Serbatoio 2 = GPL/Benzina (FuelType 110)
    df_convertito['FuelType'] = df_excel['Serbatoio'].apply(
        lambda x: 501 if x == 1 else 110
    )
    
    # Colonne senza informazioni dai dati storici (verranno popolate dopo se c'è la tabella conversione)
    df_convertito['km/l (optional)'] = ''
    df_convertito['latitude (optional)'] = np.nan
    df_convertito['longitude (optional)'] = np.nan
    df_convertito['City (optional)'] = ''
    df_convertito['Notes (optional)'] = ''
    df_convertito['Missed'] = 0
    df_convertito['StationID (optional)'] = np.nan
    df_convertito['TankCalc'] = 0.0
    df_convertito['Weather'] = ''
    
    # Salva la colonna Distro per il matching successivo
    if 'Distro' in df_excel.columns:
        df_convertito['Distro_temp'] = df_excel['Distro']
    
    # UniqueId verrà ricostruito dopo l'unione
    df_convertito['UniqueId'] = 0
    
    print(f"  → {len(df_convertito)} record convertiti")
    
    return df_convertito


def applica_conversione_distributori(df: pd.DataFrame, df_conversione: pd.DataFrame, 
                                      is_storico: bool = False) -> pd.DataFrame:
    """
    Applica la conversione dei distributori usando la tabella di conversione.
    
    Args:
        df: DataFrame da processare
        df_conversione: DataFrame con la tabella di conversione
        is_storico: True se sono dati storici (usa colonna Distro), False se sono dati Fuelio (usa StationID)
        
    Returns:
        DataFrame con i campi distributore popolati
    """
    if df_conversione is None or len(df_conversione) == 0:
        print("  ⚠ Tabella conversione non disponibile, campi distributore non popolati")
        return df
    
    print(f"\nApplicazione conversione distributori ({'dati storici' if is_storico else 'dati Fuelio'})...")
    
    # Prepara il dizionario di conversione
    if is_storico:
        # Per dati storici: usa la colonna 'Conversione' come chiave
        if 'Conversione' not in df_conversione.columns:
            print("  ⚠ Colonna 'Conversione' non trovata nella tabella")
            return df
        
        # Rimuove righe con Conversione nulla
        df_conv_clean = df_conversione.dropna(subset=['Conversione'])
        righe_rimosse = len(df_conversione) - len(df_conv_clean)
        if righe_rimosse > 0:
            print(f"  ⚠ Rimosse {righe_rimosse} righe con 'Conversione' nulla")
        
        # Rimuove duplicati, mantenendo il primo
        duplicati_prima = df_conv_clean.duplicated(subset=['Conversione']).sum()
        if duplicati_prima > 0:
            print(f"  ⚠ Trovati {duplicati_prima} duplicati in 'Conversione', uso solo il primo match")
            df_conv_clean = df_conv_clean.drop_duplicates(subset=['Conversione'], keep='first')
        
        conversione_dict = df_conv_clean.set_index('Conversione').to_dict('index')
        chiave_match = 'Distro_temp'
    else:
        # Per dati Fuelio: usa 'StationID' come chiave
        if 'StationID' not in df_conversione.columns:
            print("  ⚠ Colonna 'StationID' non trovata nella tabella")
            return df
        
        # Rimuove righe con StationID nullo
        df_conv_clean = df_conversione.dropna(subset=['StationID'])
        righe_rimosse = len(df_conversione) - len(df_conv_clean)
        if righe_rimosse > 0:
            print(f"  ⚠ Rimosse {righe_rimosse} righe con 'StationID' nullo")
        
        # Rimuove duplicati, mantenendo il primo
        duplicati_prima = df_conv_clean.duplicated(subset=['StationID']).sum()
        if duplicati_prima > 0:
            print(f"  ⚠ Trovati {duplicati_prima} duplicati in 'StationID', uso solo il primo match")
            df_conv_clean = df_conv_clean.drop_duplicates(subset=['StationID'], keep='first')
        
        conversione_dict = df_conv_clean.set_index('StationID').to_dict('index')
        chiave_match = 'StationID (optional)'
    
    # Conta i match trovati
    match_trovati = 0
    
    # Applica la conversione riga per riga
    for idx, row in df.iterrows():
        chiave = row.get(chiave_match)
        
        if pd.isna(chiave) or chiave == 0 or chiave == '':
            continue
        
        # Cerca nella tabella di conversione
        if chiave in conversione_dict:
            info_distro = conversione_dict[chiave]
            match_trovati += 1
            
            # Popola i campi del distributore
            
            # City: costruita come "NameBrand - Description"
            name_brand = info_distro.get('NameBrand', '')
            description = info_distro.get('Description', '')
            
            if pd.notna(name_brand) and pd.notna(description) and name_brand and description:
                city_value = f"{name_brand} - {description}"
                df.at[idx, 'City (optional)'] = city_value
            elif pd.notna(name_brand) and name_brand:
                # Se c'è solo NameBrand
                df.at[idx, 'City (optional)'] = name_brand
            elif pd.notna(description) and description:
                # Se c'è solo Description
                df.at[idx, 'City (optional)'] = description
            
            if 'Latitude' in info_distro and pd.notna(info_distro['Latitude']):
                df.at[idx, 'latitude (optional)'] = info_distro['Latitude']
            
            if 'Longitude' in info_distro and pd.notna(info_distro['Longitude']):
                df.at[idx, 'longitude (optional)'] = info_distro['Longitude']
            
            if 'StationID' in info_distro and pd.notna(info_distro['StationID']):
                df.at[idx, 'StationID (optional)'] = info_distro['StationID']
    
    print(f"  → Match trovati: {match_trovati}/{len(df)}")
    
    # Rimuove la colonna temporanea Distro se presente
    if 'Distro_temp' in df.columns:
        df = df.drop('Distro_temp', axis=1)
    
    return df


def unisci_e_ordina(df_storico: pd.DataFrame, df_fuelio: pd.DataFrame) -> pd.DataFrame:
    """
    Unisce i dati storici con quelli di Fuelio e ordina per data.
    
    Args:
        df_storico: DataFrame con i dati storici convertiti
        df_fuelio: DataFrame con i dati di Fuelio
        
    Returns:
        DataFrame unito e ordinato
    """
    print("\nUnione e ordinamento dati...")
    
    # Unisce i due DataFrame
    df_unito = pd.concat([df_storico, df_fuelio], ignore_index=True)
    
    # Converte la colonna Data in datetime per l'ordinamento
    df_unito['Data_temp'] = pd.to_datetime(df_unito['Data'])
    
    # Ordina per data (dal più vecchio al più recente)
    df_unito = df_unito.sort_values('Data_temp')
    
    # Ricostruisce UniqueId in ordine crescente
    df_unito['UniqueId'] = range(1, len(df_unito) + 1)
    
    # Rimuove la colonna temporanea
    df_unito = df_unito.drop('Data_temp', axis=1)
    
    # Reset dell'indice
    df_unito = df_unito.reset_index(drop=True)
    
    print(f"  → Totale record: {len(df_unito)}")
    print(f"  → Record storici: {len(df_storico)}")
    print(f"  → Record Fuelio: {len(df_fuelio)}")
    
    return df_unito


def salva_log_unificato(df: pd.DataFrame, file_output: str = "Log_unificato.csv"):
    """
    Salva il Log unificato su file CSV.
    
    Args:
        df: DataFrame con i dati unificati
        file_output: Nome del file di output
    """
    print(f"\nSalvataggio su {file_output}...")
    
    # Riordina le colonne per corrispondere al formato Log originale
    colonne_log = [
        'Data', 'Odo (km)', 'kg', 'Full', 'Price (optional)', 
        'km/l (optional)', 'latitude (optional)', 'longitude (optional)', 
        'City (optional)', 'Notes (optional)', 'Missed', 'TankNumber', 
        'FuelType', 'VolumePrice', 'StationID (optional)', 'ExcludeDistance', 
        'UniqueId', 'TankCalc', 'Weather'
    ]
    
    df = df[colonne_log]
    
    # Formattazione colonne numeriche
    print(f"  → Formattazione colonne numeriche...")
    
    # Arrotonda a 2 decimali: kg, Price (optional), VolumePrice
    colonne_2_decimali = ['kg', 'Price (optional)', 'VolumePrice']
    for col in colonne_2_decimali:
        if col in df.columns:
            df[col] = df[col].round(2)
    
    # Converte StationID a intero (mantiene NaN come NaN)
    if 'StationID (optional)' in df.columns:
        # Usa Int64 (nullable integer) per mantenere i NaN
        df['StationID (optional)'] = df['StationID (optional)'].astype('Int64')
    
    # Salva su CSV con tutte le virgolette (formato Fuelio)
    # Nota: i valori NaN (latitude, longitude, StationID nulli) vengono scritti come celle vuote nel CSV
    df.to_csv(file_output, index=False, quoting=csv.QUOTE_ALL)
    
    print(f"  → File salvato con successo!")
    print(f"  → Percorso completo: {Path(file_output).absolute()}")
    
    # Mostra statistiche finali
    print(f"\n{'='*60}")
    print("STATISTICHE FINALI")
    print(f"{'='*60}")
    print(f"Totale rifornimenti: {len(df)}")
    print(f"Periodo: dal {df['Data'].min()} al {df['Data'].max()}")
    print(f"Chilometraggio: da {df['Odo (km)'].min():.0f} km a {df['Odo (km)'].max():.0f} km")
    print(f"{'='*60}")


def main():
    """
    Funzione principale dello script.
    """
    print("="*60)
    print("UNIONE LOG STORICO CON LOG FUELIO")
    print("="*60)
    
    try:
        # 1. Carica la tabella di conversione distributori
        try:
            df_conversione = carica_tabella_conversione()
        except FileNotFoundError:
            print("  ⚠ Tabella conversione non trovata, i campi distributore non verranno popolati")
            df_conversione = None
        
        # 2. Carica i dati Excel
        df_excel = carica_dati_excel()
        
        # 3. Carica il Log di Fuelio
        df_fuelio = carica_log_fuelio()
        
        # 4. Converti i dati Excel nel formato Fuelio
        df_storico = converti_dati_excel(df_excel, df_conversione)
        
        # 5. Applica conversione distributori ai dati storici
        if df_conversione is not None:
            df_storico = applica_conversione_distributori(df_storico, df_conversione, is_storico=True)
        
        # 6. Applica conversione distributori ai dati Fuelio
        if df_conversione is not None:
            df_fuelio = applica_conversione_distributori(df_fuelio, df_conversione, is_storico=False)
        
        # 7. Unisci e ordina i dati
        df_unito = unisci_e_ordina(df_storico, df_fuelio)
        
        # 8. Salva il risultato
        salva_log_unificato(df_unito)
        
        print("\n✅ Processo completato con successo!")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERRORE: File non trovato - {e}")
        print("Assicurati che i file 'Contabilita_consumi_Punto.xlsx' e 'Log.csv' siano nella directory corrente.")
    except Exception as e:
        print(f"\n❌ ERRORE imprevisto: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
