import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter, KaplanMeierFitter
from sksurv.ensemble import RandomSurvivalForest

df = pd.read_csv("lung1_selected_for_cox.csv")

# szétválasztás
X = df.drop(columns=["patient_id", "survival_time", "event"])
y_event = df["event"]
y_time = df["survival_time"]
y_struct = np.array([(bool(e), t) for e, t in zip(y_event, y_time)],
                    dtype=[('event', bool), ('time', float)])

# Cox-modell tanítása
df_cox = df.drop(columns=["patient_id"])
cph = CoxPHFitter()
cph.fit(df_cox, duration_col="survival_time", event_col="event")

# Cox prediktált relatív kockázatok
risk_cox = cph.predict_partial_hazard(df_cox)

# RSF-modell tanítása
rsf = RandomSurvivalForest(
    n_estimators=200,
    min_samples_split=10,
    min_samples_leaf=15,
    max_features="sqrt",
    n_jobs=-1,
    random_state=42
)
rsf.fit(X, y_struct)

risk_rsf = rsf.predict(X)

cox_group = pd.qcut(risk_cox, q=2, labels=["Alacsony (Cox)", "Magas (Cox)"])
rsf_group = pd.qcut(risk_rsf, q=2, labels=["Alacsony (RSF)", "Magas (RSF)"])

# Kaplan–Meier
kmf = KaplanMeierFitter()

plt.figure(figsize=(10,7))

# Színek
colors = {
    "Alacsony (Cox)": "#0339fc",  # turkiz
    "Magas (Cox)": "#fc8803",     #  narancs
    "Alacsony (RSF)": "#119928",  #  zöld
    "Magas (RSF)": "#FF4500"      # piros
}

# Vonalstílus
linestyles = {
    "Alacsony (Cox)": "-",
    "Magas (Cox)": "-",
    "Alacsony (RSF)": "-",
    "Magas (RSF)": "-"
}

# Kaplan–Meier
for label in ["Alacsony (Cox)", "Magas (Cox)", "Alacsony (RSF)", "Magas (RSF)"]:
    if "Cox" in label:
        mask = (cox_group == label)
    else:
        mask = (rsf_group == label)
    
    kmf.fit(y_time[mask], y_event[mask], label=label)
    kmf.plot_survival_function(
        ci_show=False, 
        linestyle=linestyles[label], 
        color=colors[label]
    )

plt.title("Kaplan–Meier túlélési görbék: Cox vs RSF predikált kockázati csoportok szerint")
plt.xlabel("Túlélési idő (nap)")
plt.ylabel("Túlélési valószínűség")
plt.grid(True)
plt.tight_layout()
plt.savefig("cox_rsf_survival_overlay.png")
print("ábra elmentve: cox_rsf_survival_overlay.png")
