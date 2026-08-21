"""
api.py
=======
API REST cu FastAPI — face legătura între React și modelul Python.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from model.predictor import prezice_meci
from betting.value import compara_bookmakeri
from betting.kelly import calculeaza_pariu

app = FastAPI(title="Tennis Predictor API")

# Permitem React să comunice cu API-ul
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Modele de date ---

class CererePredictieMeci(BaseModel):
    jucator1:  str
    jucator2:  str
    suprafata: str
    rank1:     int
    rank2:     int
    cote:      Optional[dict] = None
    bankroll:  Optional[float] = 500


class CerereValoare(BaseModel):
    probabilitate: float
    cote:          dict
    bankroll:      Optional[float] = 500


# --- Endpoint-uri ---

@app.get("/")
def home():
    return {"status": "Tennis Predictor API functioneaza!"}


@app.post("/prezice")
@app.post("/prezice")
def endpoint_prezice(cerere: CererePredictieMeci):
    try:
        rez = prezice_meci(
            cerere.jucator1,
            cerere.jucator2,
            cerere.suprafata,
            cerere.rank1,
            cerere.rank2,
        )

        raspuns = {
            "jucator1":          rez["jucator1"],
            "jucator2":          rez["jucator2"],
            "suprafata":         rez["suprafata"],
            "prob_j1":           float(rez["prob_j1"]),
            "prob_j2":           float(rez["prob_j2"]),
            "castigator_prezis": rez["castigator_prezis"],
            "incredere":         float(rez["incredere"]),
            "nivel_incredere":   rez["nivel_incredere"],
            "rv_suprafata_j1":   float(rez["rv_suprafata_j1"]),
            "rv_suprafata_j2":   float(rez["rv_suprafata_j2"]),
            "forma_j1":          float(rez["forma_j1"]),
            "forma_j2":          float(rez["forma_j2"]),
            "acuratete_model":   float(rez["acuratete_model"]),
        }

        if cerere.cote:
            prob_castigator = rez["prob_j1"] if rez["castigator_prezis"] == cerere.jucator1 else rez["prob_j2"]
            rez_bookmakeri = compara_bookmakeri(float(prob_castigator), cerere.cote)
            kelly = calculeaza_pariu(
                float(prob_castigator),
                rez_bookmakeri["detalii"]["cota"],
                cerere.bankroll
            )
            raspuns["value_betting"] = {
                "bookmaker_recomandat": rez_bookmakeri["recomandat"],
                "exista_valoare":       bool(rez_bookmakeri["detalii"]["exista_valoare"]),
                "avantaj":              float(rez_bookmakeri["detalii"]["avantaj"]),
                "suma_recomandata":     float(kelly["suma"]),
                "profit_estimat":       float(kelly["profit_estimat"]),
            }

        return raspuns

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/valoare")
def endpoint_valoare(cerere: CerereValoare):
    """
    Calculează value betting și Kelly pentru cote date.
    """
    rez = compara_bookmakeri(cerere.probabilitate, cerere.cote)
    kelly = calculeaza_pariu(
        cerere.probabilitate,
        rez["detalii"]["cota"],
        cerere.bankroll
    )
    return {
        "bookmaker_recomandat": rez["recomandat"],
        "exista_valoare":       rez["detalii"]["exista_valoare"],
        "avantaj":              round(rez["detalii"]["avantaj"], 4),
        "suma_recomandata":     kelly["suma"],
        "profit_estimat":       kelly["profit_estimat"],
    }