"""
data/downloader.py
===================
Încarcă datele ATP din fișierul local.
Datele au fost descărcate manual de pe Kaggle (ATP Men's Tour)
și salvate în date_locale/atp_matches.csv
"""

import os
import pandas as pd

FOLDER_DATE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "date_locale")
FISIER_FINAL = os.path.join(FOLDER_DATE, "atp_matches.csv")


def incarca_date():
    """
    Încarcă datele din fișierul CSV local.
    Dacă fișierul nu există, îți spune exact unde să îl pui.
    """
    if not os.path.exists(FISIER_FINAL):
        print("❌ Fișierul cu date nu există!")
        print(f"   Pune fișierul atp_matches.csv în: {FOLDER_DATE}")
        return None

    print(f"📂 Se încarcă datele din {FISIER_FINAL}...")
    df = pd.read_csv(FISIER_FINAL, low_memory=False)
    print(f"✅ {len(df)} meciuri încărcate!")
    return df