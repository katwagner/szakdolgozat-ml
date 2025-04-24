#!/usr/bin/env python3
import sys
from pathlib import Path

def main(base_dir):
    base = Path(base_dir)
    # rglob rekurzívan keres
    files = list(base.rglob("*_features.csv"))
    if not files:
        print("Nincs törölni való *_features.csv fájl.")
        return

    for f in files:
        try:
            f.unlink()
            print(f"Törölve: {f}")
        except Exception as e:
            print(f"Hiba a törlésnél: {f} -> {e}")

    print(f"\nÖsszesen {len(files)} fájl törölve.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Használat: python delete_features.py /út/a/projekt/gyökérkönyvtárához")
        sys.exit(1)
    main(sys.argv[1])
