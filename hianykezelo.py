import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.read_csv("lung1_full_dataset.csv")

# Kiszűrjük azokat az oszlopokat, ahol a hiányzó értékek aránya > 20%
threshold = 0.2  # 20%
missing_ratio = df.isna().mean()
cols_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()
print("Túl sok hiányt tartalmazó oszlopok:", cols_to_drop)

df = df.drop(columns=cols_to_drop)

# Oszlopok típusok alapján szétválasztása
num_cols = df.select_dtypes(include=['float64', 'int64']).columns.drop(["survival_time", "event"], errors='ignore')
cat_cols = df.select_dtypes(include=['object', 'category']).columns.drop(["patient_id"], errors='ignore')

# Hiányzó értékek pótlása
# numerikus - medián
num_imputer = SimpleImputer(strategy="median")
df[num_cols] = num_imputer.fit_transform(df[num_cols])

# kategorikus - módusz
cat_imputer = SimpleImputer(strategy="most_frequent")
df[cat_cols] = cat_imputer.fit_transform(df[cat_cols])

# Ellenőrzés
print("Maradt hiány:", df.isna().sum().sum())

# Mentés
df.to_csv("lung1_cleaned_dataset.csv", index=False)
print("Mentve: lung1_cleaned_dataset.csv")
