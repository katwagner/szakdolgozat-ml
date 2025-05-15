import pandas as pd
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import logrank_test
from sklearn.model_selection import train_test_split

df = pd.read_csv("lung1_selected_for_cox.csv")

X_cols = df.columns.difference(["patient_id", "survival_time", "event"])

# Cox-modell tanítása a teljes adathalmazon
cph = CoxPHFitter()
cph.fit(df[["survival_time", "event"] + list(X_cols)], duration_col="survival_time", event_col="event")

# Kockázat predikció
df["risk_score"] = cph.predict_partial_hazard(df)

# Kockázati csoportok képzése
df["risk_group"] = pd.qcut(df["risk_score"], q=2, labels=["Alacsony kockázat", "Magas kockázat"])

# Kaplan–Meier túlélési görbék illesztése
kmf = KaplanMeierFitter()

plt.figure(figsize=(10, 6))
for label in df["risk_group"].unique():
    mask = df["risk_group"] == label
    kmf.fit(durations=df[mask]["survival_time"], event_observed=df[mask]["event"], label=label)
    kmf.plot_survival_function(ci_show=False)

# Ábra finomítása
plt.title("Kaplan–Meier túlélési görbék a Cox-modell predikált kockázati csoportjai szerint")
plt.xlabel("Túlélési idő (nap)")
plt.ylabel("Túlélési valószínűség")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Mentés
plt.savefig("cox_risk_groups.png")
print("Ábra elmentve: cox_risk_groups.png")

# A két kockázati csoport kiválasztása
low_risk = df[df["risk_group"] == "Alacsony kockázat"]
high_risk = df[df["risk_group"] == "Magas kockázat"]

# Log-rank teszt futtatása
results = logrank_test(
    low_risk["survival_time"], high_risk["survival_time"],
    event_observed_A=low_risk["event"],
    event_observed_B=high_risk["event"]
)

print(f"\nLog-rank teszt p-érték: {results.p_value:.4f}")
