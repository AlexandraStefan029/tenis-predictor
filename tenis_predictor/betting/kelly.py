"""
betting/kelly.py
=================
Calculează cât din bankroll să pariezi folosind Kelly Criterion.
"""


def kelly_procent(probabilitate, cota):
    """
    Formula Kelly: (probabilitate * cota - 1) / (cota - 1)
    Returnează procentul optim din bankroll.
    """
    if cota <= 1:
        raise ValueError("Cota trebuie să fie mai mare decât 1.")
    return (probabilitate * cota - 1) / (cota - 1)


def calculeaza_pariu(probabilitate, cota, bankroll, fractie=0.5):
    """
    Calculează suma recomandată de pariat.

    fractie=0.5 = Half Kelly (recomandat — mai conservator)
    fractie=1.0 = Kelly complet (agresiv, nu recomandat)
    """
    procent_kelly = kelly_procent(probabilitate, cota)

    if procent_kelly <= 0:
        return {
            "recomandare":    "NU PARIA — fara valoare",
            "suma":           0,
            "procent":        0,
            "profit_estimat": 0,
        }

    # Aplicăm fracția și limita maximă de 20%
    procent_final = min(procent_kelly * fractie, 0.20)
    suma = round(bankroll * procent_final, 2)
    profit_estimat = round(suma * (cota - 1), 2)

    return {
        "recomandare":    f"Pariaza {suma} lei ({procent_final:.1%} din bankroll)",
        "suma":           suma,
        "procent":        procent_final,
        "profit_estimat": profit_estimat,
        "kelly_complet":  procent_kelly,
    }