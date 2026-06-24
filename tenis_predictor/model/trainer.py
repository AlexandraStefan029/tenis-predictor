"""
model/trainer.py - Versiune ultra-optimizată cu pandas vectorizat
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

FOLDER_DATE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "date_locale")
FISIER_MODEL = os.path.join(FOLDER_DATE, "model.pkl")

COD_SUPRAFATA = {"Hard": 0, "Clay": 1, "Grass": 2}

COLOANE_FEATURES = [
    "diferenta_rank", "ratio_rank",
    "rv_suprafata_j1", "rv_suprafata_j2",
    "avantaj_suprafata", "forma_j1", "forma_j2",
    "avantaj_forma", "cod_suprafata",
]


def calculeaza_rv(df):
    """Rata victorie per jucator per suprafata — 100% vectorizat."""
    victorii  = df.groupby(['winner_name', 'surface']).size().reset_index(name='v')
    infrangeri = df.groupby(['loser_name',  'surface']).size().reset_index(name='i')
    infrangeri = infrangeri.rename(columns={'loser_name': 'winner_name'})

    rv = victorii.merge(infrangeri, on=['winner_name', 'surface'], how='outer').fillna(0)
    rv['total'] = rv['v'] + rv['i']
    rv['incredere'] = (rv['total'] / 25).clip(upper=1.0)
    rv['rata_bruta'] = rv['v'] / rv['total'].replace(0, 1)
    rv['rata'] = rv['incredere'] * rv['rata_bruta'] + (1 - rv['incredere']) * 0.5

    return rv.set_index(['winner_name', 'surface'])['rata'].to_dict()


def calculeaza_forma(df):
    """Forma recenta per jucator — vectorizat."""
    wins   = df.groupby('winner_name').apply(lambda x: x.tail(20)['winner_name'].count())
    losses = df.groupby('loser_name').apply(lambda x: x.tail(20)['loser_name'].count())

    toti = pd.DataFrame({'v': wins, 'i': losses}).fillna(0)
    toti['total'] = toti['v'] + toti['i']
    toti['forma'] = toti['v'] / toti['total'].replace(0, 1)

    return toti['forma'].to_dict()


def antreneaza_si_salveaza(df, esantion=5000):
    """Antrenează modelul complet vectorizat — rapid."""

    print("📊 Calculăm statistici (vectorizat)...")
    cache_rv    = calculeaza_rv(df)
    cache_forma = calculeaza_forma(df)
    print("✅ Statistici gata!")

    # Eșantion de meciuri valide
    df_valid = df[~df['intrerupt']].sample(
        min(esantion, len(df)), random_state=42
    ).copy()

    print(f"🔧 Construim features pentru {len(df_valid)} meciuri...")

    # Toate operațiile vectorizate pe DataFrame
    df_valid['rv1'] = df_valid.apply(
        lambda r: cache_rv.get((r['winner_name'], r['surface']), 0.5), axis=1
    )
    df_valid['rv2'] = df_valid.apply(
        lambda r: cache_rv.get((r['loser_name'], r['surface']), 0.5), axis=1
    )
    df_valid['f1'] = df_valid['winner_name'].map(cache_forma).fillna(0.5)
    df_valid['f2'] = df_valid['loser_name'].map(cache_forma).fillna(0.5)
    df_valid['cod'] = df_valid['surface'].map(COD_SUPRAFATA).fillna(0)

    # Perspectiva 1: câștigătorul e j1
    p1 = pd.DataFrame({
        'diferenta_rank':    df_valid['loser_rank'].values  - df_valid['winner_rank'].values,
        'ratio_rank':        df_valid['winner_rank'].values / df_valid['loser_rank'].replace(0, 1).values,
        'rv_suprafata_j1':   df_valid['rv1'].values,
        'rv_suprafata_j2':   df_valid['rv2'].values,
        'avantaj_suprafata': df_valid['rv1'].values - df_valid['rv2'].values,
        'forma_j1':          df_valid['f1'].values,
        'forma_j2':          df_valid['f2'].values,
        'avantaj_forma':     df_valid['f1'].values - df_valid['f2'].values,
        'cod_suprafata':     df_valid['cod'].values,
    })

    # Perspectiva 2: învinșul e j1 (oglindă)
    p2 = pd.DataFrame({
        'diferenta_rank':    df_valid['winner_rank'].values  - df_valid['loser_rank'].values,
        'ratio_rank':        df_valid['loser_rank'].values / df_valid['winner_rank'].replace(0, 1).values,
        'rv_suprafata_j1':   df_valid['rv2'].values,
        'rv_suprafata_j2':   df_valid['rv1'].values,
        'avantaj_suprafata': df_valid['rv2'].values - df_valid['rv1'].values,
        'forma_j1':          df_valid['f2'].values,
        'forma_j2':          df_valid['f1'].values,
        'avantaj_forma':     df_valid['f2'].values - df_valid['f1'].values,
        'cod_suprafata':     df_valid['cod'].values,
    })

    X = pd.concat([p1, p2], ignore_index=True)[COLOANE_FEATURES]
    y = pd.Series([1] * len(p1) + [0] * len(p2))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("\n🤖 Antrenăm Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200, max_depth=10,
        min_samples_leaf=5, random_state=42, n_jobs=-1,
    )
    model.fit(X_train, y_train)

    acuratete = accuracy_score(y_test, model.predict(X_test))
    print(f"✅ Acuratețe: {acuratete:.1%}")

    importante = sorted(
        zip(COLOANE_FEATURES, model.feature_importances_),
        key=lambda x: -x[1]
    )
    print("\n📊 Ce contează cel mai mult:")
    for nume, val in importante:
        print(f"   {nume:<25} {val:.1%}")

    os.makedirs(FOLDER_DATE, exist_ok=True)
    with open(FISIER_MODEL, "wb") as f:
        pickle.dump({
            "model":      model,
            "coloane":    COLOANE_FEATURES,
            "acuratete":  acuratete,
            "cache_rv":   cache_rv,
            "cache_forma": cache_forma,
        }, f)

    print(f"\n💾 Model salvat în: {FISIER_MODEL}")
    return model, acuratete