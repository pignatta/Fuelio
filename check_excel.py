import pandas as pd

df = pd.read_excel('Tabella_Conversione_Distro.xlsx', header=[2])
print("Colonne:", df.columns.tolist())
print("\nPrime righe:")
print(df.head())
print("\nUltime righe:")
print(df.tail())
print("\nInfo:")
print(df.info())
