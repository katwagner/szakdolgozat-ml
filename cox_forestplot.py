import pandas as pd
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter

df = pd.read_csv("lung1_selected_for_cox.csv")

# Cox modell tanítása (teljes adaton a vizualizációhoz)
X_cols = df.columns.difference(["patient_id", "survival_time", "event"])
cph = CoxPHFitter()
cph.fit(df[["survival_time", "event"] + list(X_cols)], duration_col="survival_time", event_col="event")

# Ábra készítése (hazard ratio + CI)
plt.figure(figsize=(6, 10))
cph.plot()
plt.title("Cox-modell hazard ráták (HR) és konfidenciaintervallumok")
plt.subplots_adjust(right=0.8)
plt.savefig("cox_forestplot.png", bbox_inches="tight")
print("Forest plot mentve: cox_forestplot.png")
