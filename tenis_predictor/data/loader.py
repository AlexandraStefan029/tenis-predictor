"""
data/loader.py
===============
Curăță și pregătește datele ATP pentru analiză.
Adaptat pentru formatul Kaggle ATP Men's Tour.
"""

import pandas as pd
import numpy as np


def incarca_si_curata(df):
    """
    Primește datele brute și le pregătește pentru analiză:
    - standardizează coloanele
    - curăță valorile lipsă
    - marchează meciurile întrerupte
    - standardizează suprafețele
    """
    df = df.copy()

    # --- Redenumim coloanele la numele standard folosit în restul aplicației ---
    df = df.rename(columns={
        'Winner':   'winner_name',
        'Loser':    'loser_name',
        'WRank':    'winner_rank',
        'LRank':    'loser_rank',
        'Surface':  'surface',
        'Date':     'tourney_date',
        'Comment':  'comment',
        'B365W':    'cota_b365_winner',
        'B365L':    'cota_b365_loser',
        'MaxW':     'cota_max_winner',
        'MaxL':     'cota_max_loser',
        'AvgW':     'cota_avg_winner',
        'AvgL':     'cota_avg_loser',
    })

    # --- Standardizăm data ---
    df['tourney_date'] = pd.to_datetime(df['tourney_date'], errors='coerce')
    df = df.dropna(subset=['tourney_date'])

    # --- Curățăm ranking-urile lipsă ---
    # Dacă un jucător nu are ranking, presupunem unul slab (300)
    df['winner_rank'] = pd.to_numeric(df['winner_rank'], errors='coerce').fillna(300)
    df['loser_rank']  = pd.to_numeric(df['loser_rank'],  errors='coerce').fillna(300)

    # --- Standardizăm suprafețele ---
    df['surface'] = df['surface'].str.strip().str.capitalize()
    df['surface'] = df['surface'].replace({'Carpet': 'Hard'})  # Carpet e rar, îl tratăm ca Hard
    df = df[df['surface'].isin(['Hard', 'Clay', 'Grass'])]

    # --- Marcăm meciurile întrerupte ---
    # "Retired" = jucătorul s-a retras; "Walkover" = n-a apărut la meci
    # Le excludem din antrenare (nu reflectă un meci normal)
    df['intrerupt'] = df['comment'].astype(str).str.contains(
        'Retired|Walkover', case=False, na=False
    )

    # --- Eliminăm rândurile fără jucători ---
    df = df.dropna(subset=['winner_name', 'loser_name'])

    # --- Sortăm cronologic ---
    df = df.sort_values('tourney_date').reset_index(drop=True)

    print(f"✅ Date curățate!")
    print(f"   Total meciuri:      {len(df)}")
    print(f"   Meciuri întrerupte: {df['intrerupt'].sum()}")
    print(f"   Suprafețe: {df['surface'].value_counts().to_dict()}")
    print(f"   Perioadă: {df['tourney_date'].min().date()} → {df['tourney_date'].max().date()}")

    return df