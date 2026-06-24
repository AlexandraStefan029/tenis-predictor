"""
model/predictor.py
===================
Încarcă modelul salvat și face predicții pentru meciuri noi.
"""

import os
import pickle
import pandas as pd
from datetime import datetime

FOLDER_DATE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "date_locale")
FISIER_MODEL = os.path.join(FOLDER_DATE, "model.pkl")


def incarca_model():
    """Încarcă modelul antrenat de pe disc."""
    if not os.path.exists(FISIER_MODEL):
        raise FileNotFoundError(
            "Nu există niciun model antrenat. "
            "Rulează mai întâi python test.py ca să antrenezi modelul."
        )
    with open(FISIER_MODEL, "rb") as f:
        date = pickle.load(f)
    return date["model"], date["coloane"], date["cache_rv"], date["cache_forma"], date["acuratete"]


def prezice_meci(jucator1, jucator2, suprafata, rank1, rank2):
    """
    Face predicția pentru un meci între doi jucători.

    Parametri:
        jucator1:  numele primului jucător (ex: "Djokovic N.")
        jucator2:  numele celui de-al doilea jucător
        suprafata: "Hard", "Clay" sau "Grass"
        rank1:     ranking ATP al primului jucător
        rank2:     ranking ATP al celui de-al doilea jucător

    Returnează un dicționar cu toate predicțiile.
    """
    model, coloane, cache_rv, cache_forma, acuratete_model = incarca_model()

    # Preluăm statisticile din cache
    rv1 = cache_rv.get((jucator1, suprafata), 0.50)
    rv2 = cache_rv.get((jucator2, suprafata), 0.50)
    f1  = cache_forma.get(jucator1, 0.50)
    f2  = cache_forma.get(jucator2, 0.50)

    # Construim features — exact ca la antrenare
    features = {
        "diferenta_rank":    rank2 - rank1,
        "ratio_rank":        rank1 / max(rank2, 1),
        "rv_suprafata_j1":   rv1,
        "rv_suprafata_j2":   rv2,
        "avantaj_suprafata": rv1 - rv2,
        "forma_j1":          f1,
        "forma_j2":          f2,
        "avantaj_forma":     f1 - f2,
        "cod_suprafata":     {"Hard": 0, "Clay": 1, "Grass": 2}.get(suprafata, 0),
    }

    X = pd.DataFrame([features])[coloane]

    # Probabilitate de câștig
    prob = model.predict_proba(X)[0]
    prob_j1 = round(prob[1], 4)
    prob_j2 = round(1 - prob_j1, 4)

    castigator_prezis = jucator1 if prob_j1 >= prob_j2 else jucator2
    incredere = max(prob_j1, prob_j2)

    if incredere >= 0.75:   nivel = "Foarte mare"
    elif incredere >= 0.65: nivel = "Mare"
    elif incredere >= 0.55: nivel = "Medie"
    else:                   nivel = "Mica - meci echilibrat"

    return {
        "jucator1":          jucator1,
        "jucator2":          jucator2,
        "suprafata":         suprafata,
        "prob_j1":           prob_j1,
        "prob_j2":           prob_j2,
        "castigator_prezis": castigator_prezis,
        "incredere":         incredere,
        "nivel_incredere":   nivel,
        "rv_suprafata_j1":   rv1,
        "rv_suprafata_j2":   rv2,
        "forma_j1":          f1,
        "forma_j2":          f2,
        "acuratete_model":   acuratete_model,
    }
    