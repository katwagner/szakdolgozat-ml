import pandas as pd

df = pd.read_csv("Lung1_clinical_data.csv")

# Átnevezés
df = df.rename(columns={
    "PatientID": "patient_id",
    "Survival.time": "survival_time",
    "deadstatus.event": "event",
    "Overall.Stage": "stage"
})

# Csak szükséges oszlopok megtartása
columns_to_keep = ["patient_id", "age", "gender", "Histology", "stage", "survival_time", "event"]
df = df[columns_to_keep]

# Típusellenőrzés és átalakítás
df["survival_time"] = pd.to_numeric(df["survival_time"], errors="coerce")
df["event"] = pd.to_numeric(df["event"], errors="coerce")

print(df.head())

# Mentés új fájlba
df.to_csv("Lung1_clinical_processed.csv", index=False)
