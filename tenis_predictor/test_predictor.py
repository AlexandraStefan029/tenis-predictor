from model.predictor import prezice_meci

rez = prezice_meci("Djokovic N.", "Nadal R.", "Hard", 2, 3)

print(f"Meci: {rez['jucator1']} vs {rez['jucator2']} ({rez['suprafata']})")
print(f"Castigator prezis: {rez['castigator_prezis']}")
print(f"Probabilitate: {rez['prob_j1']:.0%} - {rez['prob_j2']:.0%}")
print(f"Incredere: {rez['nivel_incredere']}")
print(f"Rata victorie pe Hard: {rez['rv_suprafata_j1']:.0%} vs {rez['rv_suprafata_j2']:.0%}")
