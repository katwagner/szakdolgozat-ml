import glob
import subprocess
import os
import logging

# Log
logging.basicConfig(
    filename="run_all.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Mintázat a base_dir-ekre
pattern = "LUNG1_DICOM/manifest-*/NSCLC-Radiomics/LUNG1-*/*"
bases = sorted(glob.glob(pattern))

# ─── DEBUG ───────────────────────────────────────────────────────────
print(f"Talált base_dir-ek száma: {len(bases)}")
for b in bases:
    print("  ", b)
# ─────────────────────────────────────────────────────────────────────

if not bases:
    print("Nem találok egyetlen base_dir-t sem. Ellenőrizd a mintát!")
    exit(1)

for base in bases:
    patient = os.path.basename(os.path.dirname(base))
    out_csv = os.path.join(base, f"{patient}_features.csv")

    if os.path.exists(out_csv):
        print(f"Skipping {patient}: már elkészült")
        logging.info(f"Skip {patient}")
        continue

    print(f"=== START {patient} ===")
    logging.info(f"Start {patient}")

    # DICOM - NIfTI + mask
    try:
        subprocess.run(
            ["python", "dicom_to_nifti.py", "--base_dir", base],
            check=True
        )
        logging.info(f"{patient} dicom_to_nifti OK")
    except subprocess.CalledProcessError as e:
        print(f"{patient}: dicom_to_nifti FAILED, ugorjuk")
        logging.error(f"{patient} dicom_to_nifti ERROR: {e}")
        continue

    # Radiomikai feature kinyerés
    try:
        subprocess.run([
            "pyradiomics",
            os.path.join(base, "ct.nii.gz"),
            os.path.join(base, "mask.nii.gz"),
            "--param", "params.yaml",
            "--format", "csv",        
            "--out", out_csv
        ], check=True)
        print(f"{patient}: pyradiomics OK")
        logging.info(f"{patient} pyradiomics OK")
    except subprocess.CalledProcessError as e:
        print(f"{patient}: pyradiomics FAILED, ugorjuk")
        logging.error(f"{patient} pyradiomics ERROR: {e}")
        continue

    print(f"=== DONE {patient} ===")

print("Vége – a részletek a run_all.log‑ban!")    
