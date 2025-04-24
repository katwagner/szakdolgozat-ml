from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.read_csv("lung1_cleaned_dataset.csv")

# Kiválasztjuk a numerikus oszlopokat
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
numeric_cols = numeric_cols.drop(["survival_time", "event"], errors="ignore")

X = df[numeric_cols]

# Z-score normalizálás
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Vissza DataFrame-be
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# Visszaillesztjük a target oszlopokat + patient_id
df_scaled = pd.concat([df[["patient_id", "survival_time", "event"]], X_scaled_df], axis=1)

# Mentés
df_scaled.to_csv("lung1_scaled_dataset.csv", index=False)
print("Normalizált adat mentve: lung1_scaled_dataset.csv")
