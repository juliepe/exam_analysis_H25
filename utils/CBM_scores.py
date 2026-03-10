#This file contains functions to calculate CBM scores with different mapping.
import math
import pandas as pd


def _make_score_map(scores):
    """Map answer alternatives 1–5 to scores. scores = [alt1, alt2, alt3, alt4, alt5]."""
    return {i + 1: float(s) for i, s in enumerate(scores)}


def round_to_nearest_half(num):
    """Rounds up to the nearest 0.5 interval (ceiling to nearest half)."""
    return math.ceil(num * 2) / 2


def cbm_total_score1( df, student_col='student_id', question_col='question_number', answer_col='answer_alternative', confidence_col='confidence_level', output_col='part2_cbm_score',
):
    # --- Edit score lists here to change the point mapping per question ---
    score_map_1  = _make_score_map([1,   0.5, 0.5, -1.5, -2])   # max 1 pt
    score_map_2 = _make_score_map([2,   1,   1,   -3,   -4])   # max 2 pt
    score_map_3 = _make_score_map([1,   0.5, 0.5, -1.5, -2])   # max 1 pt

    question_maps = {
        '2.1':  score_map_1,
        '2.2':  score_map_1,
        '2.3':  score_map_1,
        '2.4':  score_map_1,
        '2.5':  score_map_1,
        '2.6':  score_map_1,
        '2.7':  score_map_1,
        '2.8':  score_map_1,
        '2.9':  score_map_1,
        '2.10': score_map_2,
        '2.11': score_map_3,
        '2.12': score_map_2,
        '2.13': score_map_2,
        '2.14': score_map_2,
        '2.15': score_map_2,
    }
    # ----------------------------------------------------------------------

    df = df.copy()

    answer_nums = pd.to_numeric(df[answer_col], errors='coerce')
    score_values = [
        question_maps.get(str(q), {}).get(int(a), 0.0) if pd.notna(a) else 0.0
        for q, a in zip(df[question_col], answer_nums)
    ]
    df['_contribution'] = pd.array(score_values, dtype=float) * df[confidence_col].values

    total_per_student = df.groupby(student_col)['_contribution'].sum()
    df[output_col] = df[student_col].map(total_per_student).apply(round_to_nearest_half)
    df.drop(columns=['_contribution'], inplace=True)

    return df



def cbm_total_score2(
    df,
    student_col='student_id',
    question_col='question_number',
    answer_col='answer_alternative',
    confidence_col='confidence_level',
    output_col='part2_cbm_score',
):
    # --- Edit score lists here to change the point mapping per question ---
    score_map_1  = _make_score_map([1,   0.5, 0.5, -1.5, -2])   # max 1 pt
    score_map_2 = _make_score_map([2,   1,   1,   -3,   -4])   # max 2 pt
    score_map_3 = _make_score_map([1,   0.5, 0.5, -1.5, -2])   # max 1 pt

    question_maps = {
        '2.1':  score_map_1,
        '2.2':  score_map_1,
        '2.3':  score_map_1,
        '2.4':  score_map_1,
        '2.5':  score_map_1,
        '2.6':  score_map_1,
        '2.7':  score_map_1,
        '2.8':  score_map_1,
        '2.9':  score_map_1,
        '2.10': score_map_1,
        '2.11': score_map_1,
        '2.12': score_map_1,
        '2.13': score_map_1,
        '2.14': score_map_1,
        '2.15': score_map_1,
    }
    # ----------------------------------------------------------------------

    df = df.copy()

    answer_nums = pd.to_numeric(df[answer_col], errors='coerce')
    score_values = [
        question_maps.get(str(q), {}).get(int(a), 0.0) if pd.notna(a) else 0.0
        for q, a in zip(df[question_col], answer_nums)
    ]
    df['_contribution'] = pd.array(score_values, dtype=float) * df[confidence_col].values

    total_per_student = df.groupby(student_col)['_contribution'].sum()
    df[output_col] = df[student_col].map(total_per_student).apply(round_to_nearest_half)
    df.drop(columns=['_contribution'], inplace=True)

    return df



def cbm_total_score_exam(
    df,
    student_col='student_id',
    question_col='question_number',
    answer_col='answer_alternative',
    confidence_col='confidence_level',
    output_col='part2_cbm_score',
):
    # --- Edit score lists here to change the point mapping per question ---
    score_map_1  = _make_score_map([1,   0.5, 0.5, -1.5, -2])   # max 1 pt
    score_map_2 = _make_score_map([2,   1,   1,   -3,   -4])   # max 2 pt
    score_map_3 = _make_score_map([1,   0.5, 0.5, -1.5, -2])   # max 1 pt

    question_maps = {
        '2.1':  score_map_1,
        '2.2':  score_map_1,
        '2.3':  score_map_1,
        '2.4':  score_map_1,
        '2.5':  score_map_1,
        '2.6':  score_map_1,
        '2.7':  score_map_1,
    }
    # ----------------------------------------------------------------------

    df = df.copy()

    answer_nums = pd.to_numeric(df[answer_col], errors='coerce')
    score_values = [
        question_maps.get(str(q), {}).get(int(a), 0.0) if pd.notna(a) else 0.0
        for q, a in zip(df[question_col], answer_nums)
    ]
    df['_contribution'] = pd.array(score_values, dtype=float) * df[confidence_col].values

    total_per_student = df.groupby(student_col)['_contribution'].sum()
    df[output_col] = df[student_col].map(total_per_student).apply(round_to_nearest_half)
    df.drop(columns=['_contribution'], inplace=True)

    return df