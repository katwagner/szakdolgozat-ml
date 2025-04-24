import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

df = pd.read_csv("lung1_cleaned_dataset.csv")
df = df[df["gender"].notna()]

kmf = KaplanMeierFitter()
plt.figure(figsize=(10, 6))
p_groups = []

for gender in df["gender"].unique():
    mask = df["gender"] == gender
    kmf.fit(df[mask]["survival_time"], df[mask]["event"], label=str(gender).capitalize())
    kmf.plot_survival_function(ci_show=False)
    p_groups.append((df[mask]["survival_time"], df[mask]["event"]))

# log-rank teszt
if len(p_groups) == 2:
    dur1, ev1 = p_groups[0]
    dur2, ev2 = p_groups[1]
    result = logrank_test(dur1, dur2, event_observed_A=ev1, event_observed_B=ev2)
    print(f"Log-rank teszt p-értéke: {result.p_value:.4f}")

plt.title("Kaplan–Meier túlélési görbék nem szerint")
plt.xlabel("Túlélési idő (nap)")
plt.ylabel("Túlélési valószínűség")
plt.grid(True)
plt.tight_layout()
plt.savefig("km_gender.png")
print("km_gender.png elmentve.")
