import pandas as pd
import numpy as np
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import concordance_index_censored
from sklearn.model_selection import StratifiedKFold

df = pd.read_csv("lung1_filtered_dataset.csv")

X = df.drop(columns=["patient_id", "survival_time", "event"])
y = df[["event", "survival_time"]]
y = np.array([(bool(e), t) for e, t in zip(y["event"], y["survival_time"])],
             dtype=[('event', bool), ('time', float)])

# 5-fold
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

stratify_labels = df["event"]

c_indices = []

# Keresztvalidáció
for train_idx, test_idx in kf.split(X, stratify_labels):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    
    rsf = RandomSurvivalForest(
        n_estimators=200,
        min_samples_split=10,
        min_samples_leaf=15,
        max_features="sqrt",
        n_jobs=-1,
        random_state=42
    )
    rsf.fit(X_train, y_train)
    
    risk_scores = rsf.predict(X_test)
    c_index = concordance_index_censored(y_test["event"], y_test["time"], risk_scores)[0]
    c_indices.append(c_index)

# Átlag és szórás számítása
mean_c_index = np.mean(c_indices)
std_c_index = np.std(c_indices)

print(f"5-fold átlagos C-index: {mean_c_index:.4f} ± {std_c_index:.4f}")
