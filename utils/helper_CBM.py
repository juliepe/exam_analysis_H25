import pandas as pd


def get_cbm_valid_questions(prefix, start, end):
    """
    Build an ordered list of valid CBM question identifiers.

    Args:
        prefix (str): Question prefix, e.g. "2."
        start (int): First question number (inclusive)
        end (int): Last question number (inclusive)

    Returns:
        list[str]: Ordered list of question identifiers, e.g. ["2.1", "2.2", ..., "2.15"]
    
    Example:
        >>> get_cbm_valid_questions("2.", 1, 15)
        ['2.1', '2.2', ..., '2.15']
    """
    return [f"{prefix}{i}" for i in range(start, end + 1)]


def cast_columns_to_string(df, string_columns):
    """
    Cast specified columns to string type.

    Args:
        df (pd.DataFrame): Input DataFrame
        string_columns (list[str]): Column names to convert

    Returns:
        pd.DataFrame: DataFrame with columns cast to str
    """
    df = df.copy()
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df


def filter_cbm_questions(df, valid_questions, question_col='question_number'):
    """
    Filter DataFrame to CBM questions only and set an ordered Categorical on the question column.

    Args:
        df (pd.DataFrame): Input DataFrame
        valid_questions (list[str]): Ordered list of valid question identifiers
        question_col (str): Name of the question number column

    Returns:
        pd.DataFrame: Filtered DataFrame with ordered Categorical question column
    """
    df_cbm = df[df[question_col].isin(valid_questions)].copy()
    df_cbm[question_col] = pd.Categorical(
        df_cbm[question_col],
        categories=valid_questions,
        ordered=True
    )
    return df_cbm


def drop_columns_from_config(df, columns_to_remove):
    """
    Drop columns listed in config, ignoring any that are not present.

    Args:
        df (pd.DataFrame): Input DataFrame
        columns_to_remove (list[str]): Column names to drop

    Returns:
        pd.DataFrame: DataFrame with specified columns removed
    """
    cols_to_drop = [c for c in columns_to_remove if c in df.columns]
    return df.drop(columns=cols_to_drop)


def add_auto_score(df, student_col='student_id', question_col='question_number',
                   score_col='auto_score_per_question', output_col='auto_score'):
    """
    Compute each student's total auto score and add it as a new column.

    Deduplicates by (student, question) before summing to avoid double-counting
    when the DataFrame contains multiple rows per question (e.g. one per CBM response).

    Args:
        df (pd.DataFrame): Input DataFrame
        student_col (str): Column identifying each student
        question_col (str): Column identifying each question
        score_col (str): Column with the per-question auto score
        output_col (str): Name of the new total-score column

    Returns:
        pd.DataFrame: DataFrame with the new total auto score column added
    """
    df = df.copy()
    score_per_student = (
        df.drop_duplicates(subset=[student_col, question_col])
        .groupby(student_col)[score_col]
        .sum()
    )
    df[output_col] = df[student_col].map(score_per_student)
    return df


def split_response_cbm(df, config):
    """
    Split the CBM response column into two separate columns and drop the source.

    The source column is split on whitespace (or the configured separator) into
    ``svaralternativ`` (answer choice) and ``sikkerhetsgrad`` (confidence level),
    then the source column is removed.

    Args:
        df (pd.DataFrame): Input DataFrame
        config (dict): ``response_split`` config dict with keys:
            - ``source_column`` (str): column to split
            - ``new_columns`` (list[str]): two output column names
            - ``separator`` (str, optional): split separator, default ``" "``
            - ``drop_source`` (bool, optional): drop source column, default ``True``

    Returns:
        pd.DataFrame: DataFrame with new columns added and source column removed
    """
    df = df.copy()
    split_cfg = config['response_split']
    src = split_cfg['source_column']
    new_cols = split_cfg['new_columns']
    sep = split_cfg.get('separator', ' ')

    df[new_cols] = df[src].str.strip().str.split(sep, expand=True)

    if split_cfg.get('drop_source', True):
        df.drop(columns=[src], inplace=True)

    return df


def map_confidence_level(df, col='confidence_level'):
    """
    Map raw confidence level values to normalized weights.

    Substitutes integer confidence scores with their corresponding weights:
        5 → 100, 4 → 75, 3 → 50, 2 → 25, 1 → 0

    Args:
        df (pd.DataFrame): Input DataFrame
        col (str): Name of the confidence level column to update

    Returns:
        pd.DataFrame: DataFrame with the confidence level column replaced by mapped values
    """
    mapping = {5: 100, 4: 75, 3: 50, 2: 25, 1: 0}
    df = df.copy()
    df[col] = pd.to_numeric(df[col], errors='coerce').map(mapping)
    return df


def validate_and_remove_invalid_confidence(df, student_col='student_id',
                                           question_col='question_number',
                                           confidence_col='confidence_level',
                                           expected_sum=100):
    """
    Validate that each student's confidence levels sum to the expected value per question,
    print a summary of violations, and remove the invalid (student, question) rows.

    For each (student, question) group the confidence_level values are summed.
    If the sum differs from ``expected_sum``, the group is flagged as invalid,
    a summary is printed, and those rows are dropped from the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame (must already contain mapped confidence levels)
        student_col (str): Column identifying each student
        question_col (str): Column identifying each question
        confidence_col (str): Column with the confidence level values
        expected_sum (int): Expected sum of confidence levels per (student, question)

    Returns:
        pd.DataFrame: DataFrame with invalid (student, question) rows removed
    """
    df = df.copy()

    conf_sums = (
        df.groupby([student_col, question_col])[confidence_col]
        .sum()
        .reset_index(name='conf_sum')
    )

    invalid = conf_sums[conf_sums['conf_sum'] != expected_sum]

    if invalid.empty:
        print("All (student, question) confidence sums equal "
              f"{expected_sum}. No rows removed.")
        return df

    # Summary per question
    per_question = (
        invalid.groupby(question_col)[student_col]
        .nunique()
        .reset_index(name='num_students')
    )

    under = invalid[invalid['conf_sum'] < expected_sum]
    over = invalid[invalid['conf_sum'] > expected_sum]

    print(f"Found {invalid[student_col].nunique()} student(s) with invalid "
          f"confidence sums across {per_question.shape[0]} question(s):")
    print(f"  Under {expected_sum}: {under[student_col].nunique()} student(s)")
    print(f"  Over  {expected_sum}: {over[student_col].nunique()} student(s)")
    for _, row in per_question.iterrows():
        print(f"  Question {row[question_col]}: "
              f"{row['num_students']} student(s) with incorrect sum")

    # Mark rows that belong to invalid (student, question) pairs
    invalid_keys = invalid[[student_col, question_col]].drop_duplicates()
    invalid_keys['_remove'] = True
    df = df.merge(invalid_keys, on=[student_col, question_col], how='left')
    df = df[df['_remove'].isna()].drop(columns='_remove').reset_index(drop=True)

    return df
