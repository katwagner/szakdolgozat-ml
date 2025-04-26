import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import concordance_index_censored
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from lifelines import KaplanMeierFitter

df = pd.read_csv("lung1_filtered_dataset.csv")

# Train / Test split
X = df.drop(columns=["patient_id", "survival_time", "event"])
y = df[["event", "survival_time"]]
y = np.array([(bool(e), t) for e, t in zip(y["event"], y["survival_time"])],
             dtype=[('event', bool), ('time', float)])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y["event"], random_state=42
)

# RSF modell tanítása
rsf = RandomSurvivalForest(
    n_estimators=200,
    min_samples_split=10,
    min_samples_leaf=15,
    max_features="sqrt",
    n_jobs=-1,
    random_state=42
)

rsf.fit(X_train, y_train)

# C-index értékelése
c_index_train = concordance_index_censored(y_train["event"], y_train["time"], rsf.predict(X_train))[0]
c_index_test = concordance_index_censored(y_test["event"], y_test["time"], rsf.predict(X_test))[0]
print(f"C-index (tanító): {c_index_train:.4f}")
print(f"C-index (teszt): {c_index_test:.4f}")

# Permutációs feature importance kiszámítása
def rsf_score_func(estimator, X, y):
    risk = estimator.predict(X)
    return concordance_index_censored(y["event"], y["time"], risk)[0]

perm_importance = permutation_importance(
    rsf, X_test, y_test,
    scoring=rsf_score_func,
    n_repeats=10,
    random_state=42,
    n_jobs=-1
)

sorted_idx = perm_importance.importances_mean.argsort()[::-1]

# Feature importance ábra mentése
plt.figure(figsize=(10, 6))
plt.bar(range(15), perm_importance.importances_mean[sorted_idx[:15]], align="center")
plt.xticks(range(15), X_test.columns[sorted_idx[:15]], rotation=90)
plt.title("Random Survival Forest - Permutációs jellemző fontosság (top 15)")
plt.tight_layout()
plt.savefig("rsf_permutation_importance.png")
print("Permutációs feature importance ábra elmentve: rsf_permutation_importance.png")

# Prediktált kockázati csoportok Kaplan–Meier görbéhez
risk_scores = rsf.predict(X)
risk_qcut = pd.qcut(risk_scores, q=2, labels=["Alacsony kockázat", "Magas kockázat"])

kmf = KaplanMeierFitter()

plt.figure(figsize=(10, 6))
for group in ["Alacsony kockázat", "Magas kockázat"]:
    mask = (risk_qcut == group)
    kmf.fit(df.loc[mask, "survival_time"], df.loc[mask, "event"], label=group)
    kmf.plot_survival_function(ci_show=False)

plt.title("Kaplan–Meier túlélési görbék az RSF predikált kockázati csoportjai szerint")
plt.xlabel("Túlélési idő (nap)")
plt.ylabel("Túlélési valószínűség")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("rsf_risk_groups.png")
print("KM túlélési görbe elmentve: rsf_risk_groups.png")
