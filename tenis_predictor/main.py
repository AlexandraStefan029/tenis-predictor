"""
main.py
========
🎾 TENNIS PREDICTOR — punctul de intrare al aplicației.
Leagă toate modulele și afișează predicțiile complet.
"""

from model.predictor import prezice_meci
from betting.value import calculeaza_valoare, compara_bookmakeri
from betting.kelly import calculeaza_pariu


def afiseaza_predictie(rez, cote_bookmakeri=None, bankroll=500):
    """Afișează predicția într-un format clar și complet."""

    j1 = rez['jucator1']
    j2 = rez['jucator2']
    p1 = rez['prob_j1']
    p2 = rez['prob_j2']

    sep = "=" * 55

    print(f"\n{sep}")
    print(f"  🎾  {j1}  vs  {j2}  ({rez['suprafata']})")
    print(sep)

    # Câștigătorul prezis
    print(f"\n  🏆  Castigator prezis: {rez['castigator_prezis']}")
    print(f"  📊  Incredere: {rez['nivel_incredere']} ({rez['incredere']:.0%})")

    # Bara vizuală
    bara1 = "█" * round(p1 * 40)
    bara2 = "░" * (40 - round(p1 * 40))
    print(f"\n  {j1:<28} {p1:>5.0%}")
    print(f"  [{bara1}{bara2}]")
    print(f"  {j2:<28} {p2:>5.0%}")

    # Statistici
    print(f"\n  {'─' * 53}")
    print(f"  📈  Rata victorie pe {rez['suprafata']}:")
    print(f"      {j1}: {rez['rv_suprafata_j1']:.0%}")
    print(f"      {j2}: {rez['rv_suprafata_j2']:.0%}")
    print(f"\n  🔥  Forma recenta:")
    print(f"      {j1}: {rez['forma_j1']:.0%}")
    print(f"      {j2}: {rez['forma_j2']:.0%}")

    # Value betting
    if cote_bookmakeri:
        print(f"\n  {'─' * 53}")
        print(f"  💰  ANALIZA PARIU")

        prob_castigator = p1 if rez['castigator_prezis'] == j1 else p2

        if len(cote_bookmakeri) == 1:
            bookmaker = list(cote_bookmakeri.keys())[0]
            cota = list(cote_bookmakeri.values())[0]
            val = calculeaza_valoare(prob_castigator, cota)

            print(f"\n  Probabilitate model:    {val['probabilitate_model']:.0%}")
            print(f"  Probabilitate implicita: {val['probabilitate_implicita']:.0%}")

            if val['exista_valoare']:
                print(f"  ✅  VALUE BET! Avantaj: +{val['avantaj']:.0%}")
                kelly = calculeaza_pariu(prob_castigator, cota, bankroll)
                print(f"\n  📌  {kelly['recomandare']}")
                print(f"  💵  Profit estimat daca castigi: +{kelly['profit_estimat']} lei")
            else:
                print(f"  ❌  Fara valoare ({val['avantaj']:+.0%}) — nu paria!")
        else:
            rez_bookmakeri = compara_bookmakeri(prob_castigator, cote_bookmakeri)
            print(f"\n  Bookmaker recomandat: {rez_bookmakeri['recomandat']}")
            det = rez_bookmakeri['detalii']

            if det['exista_valoare']:
                print(f"  ✅  VALUE BET! Avantaj: +{det['avantaj']:.0%}")
                kelly = calculeaza_pariu(prob_castigator, det['cota'], bankroll)
                print(f"  📌  {kelly['recomandare']}")
                print(f"  💵  Profit estimat: +{kelly['profit_estimat']} lei")
            else:
                print(f"  ❌  Fara valoare — nu paria!")

    print(f"\n{sep}")
    print(f"  ⚠️  Pariati responsabil!")
    print(sep)


def main():
    print("=" * 55)
    print("  🎾  TENNIS PREDICTOR")
    print("  Predictii bazate pe Machine Learning")
    print("=" * 55)

    # ================================================
    # MECIURI DE PREZIS
    # Modifica aici cu meciurile care te intereseaza!
    # Format: (Jucator1, Jucator2, Suprafata, Rank1, Rank2)
    # ================================================
    meciuri = [
        ("Djokovic N.", "Nadal R.",    "Hard",  2,  3),
        ("Alcaraz C.",  "Sinner J.",   "Grass", 3,  1),
        ("Medvedev D.", "Zverev A.",   "Hard",  4,  5),
    ]

    # Cotele de la bookmakeri pentru primul jucator
    # Poti adauga mai multi bookmakeri
    cote_exemplu = {
        "Betano":   2.10,
        "Superbet": 2.05,
        "Unibet":   2.20,
    }

    bankroll = 500  # lei

    for j1, j2, suprafata, r1, r2 in meciuri:
        rez = prezice_meci(j1, j2, suprafata, r1, r2)
        afiseaza_predictie(rez, cote_exemplu, bankroll)


if __name__ == "__main__":
    main()