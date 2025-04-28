import matplotlib.pyplot as plt
import numpy as np

# Modell nevei
models = ["Cox-modell", "RSF (5-fold)"]

# Átlagos C-index értékek
c_indices = [0.578, 0.5715]

# Hibasávok 
errors = [np.nan, 0.0321]

# Színek
colors = ["#FFEB99", "#A8E6CF"]

# Ábra készítése
plt.figure(figsize=(8,6))
bars = plt.bar(models, c_indices, yerr=errors, capsize=8, color=colors, edgecolor="black")
plt.ylabel("C-index")
plt.title("Cox-modell és Random Survival Forest összehasonlítása (C-index)")
plt.ylim(0.5, 0.65)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, bar in enumerate(bars):
    if np.isnan(errors[i]):
        bar.errorbar = None 

plt.tight_layout()
plt.savefig("cindex_comparison_fixed.png")
print("Új ábra elmentve: cindex_comparison_fixed.png")
