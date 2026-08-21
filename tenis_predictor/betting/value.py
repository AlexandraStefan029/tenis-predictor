"""
betting/value.py
=================
Verifică dacă există valoare într-un pariu.
Value bet = probabilitatea ta > probabilitatea implicată de cotă.
"""


def probabilitate_din_cota(cota):
    """
    Transformă o cotă europeană în probabilitate.
    Ex: cota 2.10 → 1/2.10 = 47.6%
    """
    if cota <= 1:
        raise ValueError("Cota trebuie să fie mai mare decât 1.")
    return round(1 / cota, 4)


def calculeaza_valoare(probabilitate_model, cota):
    """
    Compară probabilitatea modelului cu cea implicată de cotă.

    Ex: model zice 65%, cota implică 48% → avantaj +17% → VALUE BET!
    """
    prob_implicita = probabilitate_din_cota(cota)
    avantaj = round(probabilitate_model - prob_implicita, 4)

    return {
        "cota":                  cota,
        "probabilitate_model":   probabilitate_model,
        "probabilitate_implicita": prob_implicita,
        "avantaj":               avantaj,
        "exista_valoare":        avantaj > 0,
    }


def compara_bookmakeri(probabilitate_model, cote: dict):
    """
    Compară cotele de la mai mulți bookmakeri și găsește
    unde există cea mai mare valoare.

    cote = {"Betano": 2.10, "Superbet": 2.05, "Unibet": 2.15}
    """
    rezultate = {}
    for bookmaker, cota in cote.items():
        rezultate[bookmaker] = calculeaza_valoare(probabilitate_model, cota)

    # Cel mai bun bookmaker = avantajul cel mai mare
    cel_mai_bun = max(rezultate.items(), key=lambda x: x[1]["avantaj"])

    return {
        "toate":        rezultate,
        "recomandat":   cel_mai_bun[0],
        "detalii":      cel_mai_bun[1],
    }