import pandas as pd

# Betöltés
df = pd.read_csv("Lung1_clinical_data.csv")

# Áttekintés
print("Adatméret:", df.shape)
print("Oszlopok:", df.columns.tolist())
print("\nElső 5 sor:\n", df.head())
