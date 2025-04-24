import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

df = pd.read_csv("lung1_cleaned_dataset.csv")
df = df[df['stage'].notna()].copy()

kmf = KaplanMeierFitter()
plt.figure(figsize=(10, 6))
colors = plt.cm.tab10.colors
p_groups = []

stages = sorted(df["stage"].unique())
for i, stage in enumerate(stages):
    mask = df["stage"] == stage
    kmf.fit(durations=df[mask]["survival_time"], event_observed=df[mask]["event"], label=f"Stage {stage}")
    kmf.plot_survival_function(ci_show=False, color=colors[i % len(colors)])
    p_groups.append((df[mask]["survival_time"], df[mask]["event"]))

# log-rank teszt
if len(p_groups) >= 2:
    from itertools import combinations
    pvals = []
    for (dur1, ev1), (dur2, ev2) in combinations(p_groups, 2):
        result = logrank_test(dur1, dur2, event_observed_A=ev1, event_observed_B=ev2)
        pvals.append(result.p_value)
    overall_p = min(pvals)
    print(f"Minimum log-rank p-érték a csoportok között: {overall_p:.4f}")

plt.title("Kaplan–Meier túlélési görbék klinikai stádium szerint")
plt.xlabel("Túlélési idő (nap)")
plt.ylabel("Túlélési valószínűség")
plt.grid(True)
plt.tight_layout()
plt.savefig("km_stage.png")
print("km_stage.png elmentve.")
