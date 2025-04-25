import pandas as pd
from lifelines import CoxPHFitter
from sklearn.model_selection import train_test_split

df = pd.read_csv("lung1_selected_for_cox.csv")

X_cols = df.columns.difference(["patient_id", "survival_time", "event"])

# Tanító / teszt szétválasztás (70–30%)
train_df, test_df = train_test_split(
    df,
    test_size=0.3,
    stratify=df["event"],
    random_state=42
)

# Modell tanítása
cph = CoxPHFitter()
cph.fit(train_df[["survival_time", "event"] + list(X_cols)], duration_col="survival_time", event_col="event")

# Eredmények kiírása
cph.print_summary()

# C-index számítása a tesztkészleten
c_index = cph.score(test_df[["survival_time", "event"] + list(X_cols)], scoring_method="concordance_index")
print(f"\nC-index (tesztkészlet): {c_index:.4f}")
