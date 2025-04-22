import os
import glob
import argparse
import pydicom
import numpy as np
import SimpleITK as sitk
from skimage.draw import polygon
from scipy.ndimage import binary_fill_holes

# Argumentum feldolgozása
parser = argparse.ArgumentParser()
parser.add_argument("--base_dir", required=True,
    help="A beteg DICOM + RTSTRUCT könyvtárának a gyökérkönyvtára")
args = parser.parse_args()
base_dir = args.base_dir

# Almappák listázása a base_dir alatt
first_level = [d for d in os.listdir(base_dir)
               if os.path.isdir(os.path.join(base_dir, d))]
if len(first_level) == 1:
    new_dir = os.path.join(base_dir, first_level[0])
    base_dir = new_dir

subdirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir)
           if os.path.isdir(os.path.join(base_dir, d))]

# CT-könyvtár automatikus detektálása (legtöbb .dcm fájl)
ct_dir = max(subdirs, key=lambda d: len(glob.glob(os.path.join(d, "*.dcm"))))
print(f"CT könyvtár: {ct_dir}")

# RTSTRUCT fájl automatikus detektálása
rtstruct_path = None
for d in subdirs:
    # kihagyjuk a „Segmentation” nevű mappákat
    if "segmentation" in os.path.basename(d).lower():
        continue
    dcms = glob.glob(os.path.join(d, "*.dcm"))
    if len(dcms) == 1:
        # ellenőrizzük, hogy ez tényleg RTSTRUCT
        ds = pydicom.dcmread(dcms[0], stop_before_pixels=True)
        if getattr(ds, "Modality", "").upper() == "RTSTRUCT":
            rtstruct_path = dcms[0]
            break

if rtstruct_path is None:
    raise FileNotFoundError("Nem találtam RTSTRUCT fájlt!")

print(f"RTSTRUCT fájl: {rtstruct_path}")

# CT beolvasása és mentése .nii.gz-be
ct_files = sorted([os.path.join(ct_dir, f) for f in os.listdir(ct_dir) if f.lower().endswith(".dcm")])
reader = sitk.ImageSeriesReader()
reader.SetFileNames(ct_files)
ct_image = reader.Execute()
sitk.WriteImage(ct_image, os.path.join(base_dir, "ct.nii.gz"))
print("CT elmentve.")

# RTSTRUCT beolvasása
ds = pydicom.dcmread(rtstruct_path)


# ROI megkeresése a StructureSetROISequence-ben
roi_number = None
for roi in ds.StructureSetROISequence:
    name = roi.ROIName.lower()
    if "gtv" in name:
        roi_number = roi.ROINumber
        target_label = roi.ROIName  # megtartjuk az eredeti nevet is
        break
if roi_number is None:
    raise ValueError("Nem találtam GTV kontúrt az RTSTRUCT-ban!")

print(f"ROI kiválasztva: {target_label} (ROINumber={roi_number})")


# A hozzá tartozó ContourSequence megtalálása
contours_seq = None
for rc in ds.ROIContourSequence:
    if rc.ReferencedROINumber == roi_number:
        contours_seq = rc.ContourSequence
        break
if contours_seq is None:
    raise ValueError(f"Nincsenek kontúrok a '{target_label}' ROI-hoz.")

# Maszk inicializálása
spacing = ct_image.GetSpacing()   # (dx, dy, dz)
origin  = ct_image.GetOrigin()    # (ox, oy, oz)
size    = ct_image.GetSize()      # (nx, ny, nz)
nz, ny, nx = size[2], size[1], size[0]

mask = np.zeros((nz, ny, nx), dtype=np.uint8)

# Kontúrok síkban történő kitöltése
for contour in contours_seq:
    pts = np.array(contour.ContourData).reshape(-1, 3)
    # A szelet síkjának Z‐világkoordinátája
    z_world = pts[0, 2]
    dz = spacing[2]
    oz = origin[2]

    # Ha a DZ negatív, fordítsuk meg a képletet
    if dz > 0:
        z = int(round((z_world - oz) / dz))
    else:
        z = int(round((oz - z_world) / abs(dz)))

    # clamp Z‐index
    z = max(0, min(nz-1, z))

    # X/Y pixelek
    xs = ((pts[:, 0] - origin[0]) / spacing[0]).round().astype(int)
    ys = ((pts[:, 1] - origin[1]) / spacing[1]).round().astype(int)
    # clamp X/Y‑t is opcionálisan:
    xs = np.clip(xs, 0, nx-1)
    ys = np.clip(ys, 0, ny-1)

    # poligon‐kitöltés
    rr, cc = polygon(ys, xs, shape=(ny, nx))
    mask[z, rr, cc] = 1

# Maszk mentése
mask_img = sitk.GetImageFromArray(mask)
mask_img.SetSpacing(spacing)
mask_img.SetOrigin(origin)
mask_img.SetDirection(ct_image.GetDirection())
sitk.WriteImage(mask_img, os.path.join(base_dir, "mask.nii.gz"))
print("Poligontöltéssel készült maszk elmentve.")
