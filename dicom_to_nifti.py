import os
import pydicom
import numpy as np
import SimpleITK as sitk

# ----- Elérési útvonalak -----
base_dir = "/Users/katwagner/Documents/szakdolgozat-ml/LUNG1_DICOM/manifest-1603198545583/NSCLC-Radiomics/LUNG1-001/09-18-2008-StudyID-NA-69331"
ct_dir = os.path.join(base_dir, "0.000000-NA-82046")
rtstruct_path = os.path.join(base_dir, "3.000000-NA-78236", "1-1.dcm")

# 1) CT beolvasása és mentése .nii.gz-be
ct_files = sorted([os.path.join(ct_dir, f) for f in os.listdir(ct_dir) if f.lower().endswith(".dcm")])
reader = sitk.ImageSeriesReader()
reader.SetFileNames(ct_files)
ct_image = reader.Execute()
sitk.WriteImage(ct_image, os.path.join(base_dir, "ct.nii.gz"))
print("CT elmentve.")

# 2) RTSTRUCT beolvasása
ds = pydicom.dcmread(rtstruct_path)

# 3) ROI megkeresése a StructureSetROISequence-ben
target_label = "GTV-1"
roi_number = None
for roi in ds.StructureSetROISequence:
    if roi.ROIName.upper() == target_label.upper():
        roi_number = roi.ROINumber
        break
if roi_number is None:
    raise ValueError(f"'{target_label}' ROI nem található.")

print(f"ROI '{target_label}' azonosítója: {roi_number}")

# 4) A hozzá tartozó ContourSequence megtalálása
contours_seq = None
for rc in ds.ROIContourSequence:
    if rc.ReferencedROINumber == roi_number:
        contours_seq = rc.ContourSequence
        break
if contours_seq is None:
    raise ValueError(f"Nincsenek kontúrok a '{target_label}' ROI-hoz.")

# 5) Maszk generálása a pontokból
spacing = ct_image.GetSpacing()
origin  = ct_image.GetOrigin()
size    = ct_image.GetSize()

mask = np.zeros((size[2], size[1], size[0]), dtype=np.uint8)

for contour in contours_seq:
    # ContourData laposan tartalmazza [x1,y1,z1, x2,y2,z2, ...]
    pts = np.array(contour.ContourData).reshape(-1, 3)
    for x_world, y_world, z_world in pts:
        x = int(round((x_world - origin[0]) / spacing[0]))
        y = int(round((y_world - origin[1]) / spacing[1]))
        z = int(round((z_world - origin[2]) / spacing[2]))
        if 0 <= x < mask.shape[2] and 0 <= y < mask.shape[1] and 0 <= z < mask.shape[0]:
            mask[z, y, x] = 1

# 6) SimpleITK képbe csomagolás és mentés
mask_img = sitk.GetImageFromArray(mask)
mask_img.SetSpacing(spacing)
mask_img.SetOrigin(origin)
mask_img.SetDirection(ct_image.GetDirection())

sitk.WriteImage(mask_img, os.path.join(base_dir, "mask.nii.gz"))
print("Maszk elmentve.")
