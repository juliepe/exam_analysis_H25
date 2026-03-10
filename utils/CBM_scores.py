#This file contains functions to calculate CBM scores with different mapping.
import math
import pandas as pd

# Scoring matrices: maps answer_alternative (1–5) to score value
_SCORE_MAP_1PT = {1: 1.0, 2: 0.5, 3: 0.5, 4: -1.5, 5: -2.0}
_SCORE_MAP_2PT = {1: 2.0, 2: 1.0, 3: 1.0, 4: -3.0, 5: -4.0}

# Per-question scoring map for part 2 (questions 2.1 – 2.15)
_PART2_QUESTION_MAPS = {
    **{f'2.{i}': _SCORE_MAP_1PT for i in range(1, 10)},   # 2.1 – 2.9: max 1 pt
    '2.10': _SCORE_MAP_2PT,                                 # 2.10: max 2 pt
    '2.11': _SCORE_MAP_1PT,                                 # 2.11: max 1 pt
    **{f'2.{i}': _SCORE_MAP_2PT for i in range(12, 16)},   # 2.12 – 2.15: max 2 pt
}

def round_to_nearest_half(num):
  """Rounds up to the nearest 0.5 interval (ceiling to nearest half)."""
  return math.ceil(num * 2) / 2

def add_part2_cbm_score(
    df,
    student_col='student_id',
    question_col='question_number',
    answer_col='answer_alternative',
    confidence_col='confidence_level',
    output_col='part2_cbm_score',
):
    """
    Compute the total CBM score for part 2 (questions 2.1–2.15) and add it as a new column.

    For every row the score contribution is:
        score_map[answer_alternative] * confidence_level

    where the score_map depends on the question (1-point scale for 2.1–2.9 and 2.11,
    2-point scale for 2.10 and 2.12–2.15).

    The total score per student is the sum of all contributions across every row
    (i.e. every answer alternative for every question).

    Args:
        df (pd.DataFrame): CBM-format DataFrame (one row per answer alternative per question).
        student_col (str): Column identifying each student.
        question_col (str): Column identifying each question.
        answer_col (str): Column with the selected answer alternative (integer 1–5).
        confidence_col (str): Column with the (already mapped) confidence-level weight.
        output_col (str): Name of the new total-score column.

    Returns:
        pd.DataFrame: Copy of df with the new score column added.
    """
    df = df.copy()

    answer_nums = pd.to_numeric(df[answer_col], errors='coerce')
    score_values = [
        _PART2_QUESTION_MAPS.get(str(q), {}).get(int(a), 0.0) if pd.notna(a) else 0.0
        for q, a in zip(df[question_col], answer_nums)
    ]
    df['_contribution'] = pd.array(score_values, dtype=float) * df[confidence_col].values

    total_per_student = df.groupby(student_col)['_contribution'].sum()
    df[output_col] = df[student_col].map(total_per_student).apply(round_to_nearest_half)
    df.drop(columns=['_contribution'], inplace=True)

    return df

