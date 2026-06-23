"""
stats/engine.py
================
Calculează toate statisticile unui jucător:
- rata de victorie pe suprafață
- forma recentă
- head-to-head
- zile de odihnă (oboseală)
"""

import pandas as pd
import numpy as np

# Câte meciuri are nevoie un jucător ca să avem
# încredere deplină în statisticile lui.
# Sub această valoare, "amestecăm" cu media circuitului (50%).
MECIURI_PENTRU_INCREDERE = 25


def rata_victorie_pe_suprafata(df, jucator, suprafata):
    """
    Calculează rata de victorie pe o suprafață specifică.
    Aplică regresie către medie pentru jucătorii cu puține meciuri.

    Returnează: (rata, nr_meciuri, incredere)
    """
    meciuri = df[df['surface'] == suprafata]
    victorii  = (meciuri['winner_name'] == jucator).sum()
    infrangeri = (meciuri['loser_name'] == jucator).sum()
    total = victorii + infrangeri

    if total == 0:
        return 0.50, 0, 0.0

    rata_bruta = victorii / total
    incredere  = min(total / MECIURI_PENTRU_INCREDERE, 1.0)

    # Cu cât are mai puține meciuri, cu atât ne apropiem de 50%
    rata_ajustata = incredere * rata_bruta + (1 - incredere) * 0.50

    return round(rata_ajustata, 4), int(total), round(incredere, 2)


def forma_recenta(df, jucator, nr_meciuri=10, pana_la_data=None):
    """
    Procentul de victorii din ultimele N meciuri.
    pana_la_data: ignoră meciurile după această dată
    (evităm să "vedem în viitor" la antrenare).
    """
    mask = (
        (df['winner_name'] == jucator) |
        (df['loser_name']  == jucator)
    )
    meciuri_jucator = df[mask]

    if pana_la_data is not None:
        meciuri_jucator = meciuri_jucator[
            meciuri_jucator['tourney_date'] < pana_la_data
        ]

    recente = meciuri_jucator.tail(nr_meciuri)

    if len(recente) == 0:
        return 0.50

    victorii = (recente['winner_name'] == jucator).sum()
    return round(victorii / len(recente), 4)


def head_to_head(df, jucator1, jucator2, suprafata=None):
    """
    Istoricul direct dintre doi jucători.
    Opțional filtrat pe o suprafață specifică.

    Returnează: (rata_victorie_j1, victorii_j1, victorii_j2)
    """
    mask = (
        ((df['winner_name'] == jucator1) & (df['loser_name'] == jucator2)) |
        ((df['winner_name'] == jucator2) & (df['loser_name'] == jucator1))
    )
    meciuri = df[mask]

    if suprafata:
        meciuri = meciuri[meciuri['surface'] == suprafata]

    if len(meciuri) == 0:
        return 0.50, 0, 0

    v1 = (meciuri['winner_name'] == jucator1).sum()
    v2 = len(meciuri) - v1
    return round(v1 / len(meciuri), 4), int(v1), int(v2)


def zile_odihna(df, jucator, data_meci):
    """
    Câte zile s-au scurs de la ultimul meci al jucătorului.
    Un jucător odihnit tinde să performeze mai bine.
    """
    mask = (
        ((df['winner_name'] == jucator) | (df['loser_name'] == jucator)) &
        (df['tourney_date'] < data_meci)
    )
    meciuri_anterioare = df[mask]

    if len(meciuri_anterioare) == 0:
        return 14  # valoare neutră dacă nu avem istoric

    ultima_data = meciuri_anterioare['tourney_date'].max()
    zile = (data_meci - ultima_data).days
    return min(int(zile), 30)  # plafonăm la 30


def statistici_jucator(df, jucator, suprafata, ranking, pana_la_data=None):
    """
    Adună toate statisticile unui jucător într-un singur loc.
    Aceasta e funcția principală apelată de model și predictor.
    """
    df_context = df
    if pana_la_data is not None:
        df_context = df[df['tourney_date'] < pana_la_data]

    rata, nr_meciuri, incredere = rata_victorie_pe_suprafata(
        df_context, jucator, suprafata
    )
    forma = forma_recenta(df_context, jucator, pana_la_data=pana_la_data)
    odihna = zile_odihna(df, jucator, pana_la_data) if pana_la_data else 14

    return {
        'nume':                     jucator,
        'ranking':                  ranking,
        'rata_victorie_suprafata':  rata,
        'nr_meciuri_suprafata':     nr_meciuri,
        'incredere_statistica':     incredere,
        'forma_recenta':            forma,
        'zile_odihna':              odihna,
    }