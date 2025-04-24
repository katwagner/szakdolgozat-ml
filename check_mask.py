import numpy as np
import SimpleITK as sitk

mask = sitk.ReadImage("/Users/katwagner/Documents/szakdolgozat-ml/LUNG1_DICOM/manifest-1603198545583/NSCLC-Radiomics/LUNG1-001/09-18-2008-StudyID-NA-69331/mask.nii.gz")
arr = sitk.GetArrayFromImage(mask)
print("Unique values:", np.unique(arr))
print("Nonzero voxels:", np.count_nonzero(arr))
