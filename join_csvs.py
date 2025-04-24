import pandas as pd
from pathlib import Path

def read_pyradiomics_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Megkeressük az első olyan sort, ami valószínűleg a header
    header_line = None
    for i, line in enumerate(lines):
        if line.lower().startswith("image,") or "original_" in line:
            header_line = i
            break

    if header_line is None:
        raise ValueError(f"Nem található header: {path}")

    # A header sortól kezdjük beolvasni
    return pd.read_csv(path, skiprows=header_line)

# Klinikai adatok
cli = pd.read_csv("lung1_clinical_processed.csv")

# Radiomikai feature-ök rekurzív begyűjtése
base = Path(".")
feature_paths = sorted(base.rglob("*_features.csv"))

print(f"Talált feature-fájlok száma: {len(feature_paths)}")
for p in feature_paths:
    print(" •", p)


# Betöltés és patient_id beszúrás
seen = set()
dfs = []
for p in feature_paths:
    pid = p.stem.replace("_features", "")
    if pid in seen:
        print(f"Duplikátum, kihagyjuk: {p}")
        continue
    seen.add(pid)
    try:
        df_feat = read_pyradiomics_csv(p)
    except Exception as e:
        print(f"Nem sikerült beolvasni: {p} ({e})")
        continue
    df_feat.insert(0, "patient_id", pid)
    dfs.append(df_feat)

rad = pd.concat(dfs, ignore_index=True)

# Összekapcsolás
full = cli.merge(rad, on="patient_id", how="inner")
print("Merged shape:", full.shape)

# Mentés
full.to_csv("lung1_full_dataset.csv", index=False)
print("lung1_full_dataset.csv elkészült.")
