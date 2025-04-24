import pandas as pd
from lifelines import CoxPHFitter

df = pd.read_csv("lung1_filtered_dataset.csv")
features = df.drop(columns=["patient_id", "survival_time", "event"]).columns
selected_features = []

for col in features:
    try:
        cph = CoxPHFitter()
        cph.fit(df[[col, "survival_time", "event"]], duration_col="survival_time", event_col="event")
        p_value = cph.summary.loc[col, "p"]
        if p_value < 0.05:
            selected_features.append(col)
    except Exception as e:
        print(f"Hiba a(z) {col} oszlopnál: {e}")

df_selected = pd.concat([df[["patient_id", "survival_time", "event"]], df[selected_features]], axis=1)
df_selected.to_csv("lung1_selected_for_cox.csv", index=False)
print("lung1_selected_for_cox.csv mentve.")
print(f"Kiválasztott jellemzők száma: {len(selected_features)}")
