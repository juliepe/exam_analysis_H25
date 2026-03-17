def CBM_score_per_task_konte(df, question_number, map_answers):
    """
    Calculate total CBM score per student for a given question.

    Parameters:
        df: DataFrame with columns student_id, question_number, answer_alternative, confidence_level
        question_number: the question number
        map_answers: list of letters e.g. ['R', 'P', 'P', 'M', 'F'] mapping each answer alternative (1-indexed) to a scoring array

    Returns:
        DataFrame with columns student_id and score for the given question
    """

    # CBM point matrix
    R = [2, 4, 6, 8]
    P = [1, 2, 3, 4]
    M = [0, -4, -8, -12]
    F = [-1, -6, -11, -16]

    SCORE_MAP = {'R': R, 'P': P, 'M': M, 'F': F}
    CONFIDENCE_TO_INDEX = {25: 0, 50: 1, 75: 2, 100: 3}

    task_df = df[df['question_number'] == question_number].copy()

    def score_row(row):
        alt = int(row['answer_alternative'])
        confidence = int(row['confidence_level'])
        if confidence == 0:
            return 0
        letter = map_answers[alt - 1]
        score_array = SCORE_MAP[letter]
        return score_array[CONFIDENCE_TO_INDEX[confidence]]

    task_df['score'] = task_df.apply(score_row, axis=1)
    return task_df.groupby('student_id', as_index=False)['score'].sum()

def CBM_score_per_task_konte_no_F(df, question_number, map_answers):
    """
    Calculate total CBM score per student for a given question.

    Parameters:
        df: DataFrame with columns student_id, question_number, answer_alternative, confidence_level
        question_number: the question number
        map_answers: list of letters e.g. ['R', 'P', 'P', 'M', 'F'] mapping each answer alternative (1-indexed) to a scoring array

    Returns:
        DataFrame with columns student_id and score for the given question
    """

    # CBM point matrix, M and F is the same since F is not used
    R = [2, 4, 6, 8]
    P = [1, 2, 3, 4]
    M = [0, -4, -8, -12]
    F = [0, -4, -8, -12]

    SCORE_MAP = {'R': R, 'P': P, 'M': M, 'F': F}
    CONFIDENCE_TO_INDEX = {25: 0, 50: 1, 75: 2, 100: 3}

    task_df = df[df['question_number'] == question_number].copy()

    def score_row(row):
        alt = int(row['answer_alternative'])
        confidence = int(row['confidence_level'])
        if confidence == 0:
            return 0
        letter = map_answers[alt - 1]
        score_array = SCORE_MAP[letter]
        return score_array[CONFIDENCE_TO_INDEX[confidence]]

    task_df['score'] = task_df.apply(score_row, axis=1)
    return task_df.groupby('student_id', as_index=False)['score'].sum()

def CBM_score_per_task_konte_no_minus_points(df, question_number, map_answers):
    """
    Calculate total CBM score per student for a given question.

    Parameters:
        df: DataFrame with columns student_id, question_number, answer_alternative, confidence_level
        question_number: the question number
        map_answers: list of letters e.g. ['R', 'P', 'P', 'M', 'F'] mapping each answer alternative (1-indexed) to a scoring array

    Returns:
        DataFrame with columns student_id and score for the given question
    """

    # CBM point matrix, M and F is the same since F is not used
    R = [2, 4, 6, 8]
    P = [1, 2, 3, 4]
    M = [0, 0, 0, 0]
    F = [0, 0, 0, 0]

    SCORE_MAP = {'R': R, 'P': P, 'M': M, 'F': F}
    CONFIDENCE_TO_INDEX = {25: 0, 50: 1, 75: 2, 100: 3}

    task_df = df[df['question_number'] == question_number].copy()

    def score_row(row):
        alt = int(row['answer_alternative'])
        confidence = int(row['confidence_level'])
        if confidence == 0:
            return 0
        letter = map_answers[alt - 1]
        score_array = SCORE_MAP[letter]
        return score_array[CONFIDENCE_TO_INDEX[confidence]]

    task_df['score'] = task_df.apply(score_row, axis=1)
    return task_df.groupby('student_id', as_index=False)['score'].sum()


def CBM_score_per_task_exam(df, question_number, map_answers):
    """
    Calculate total CBM score per student for a given question.

    Parameters:
        df: DataFrame with columns student_id, question_number, answer_alternative, confidence_level
        question_number: the question number
        map_answers: list of letters e.g. ['R', 'P', 'P', 'M', 'F'] mapping each answer alternative (1-indexed) to a scoring array

    Returns:
        DataFrame with columns student_id and score for the given question
    """

    # CBM point matrix
    R = [2, 4, 6, 8]
    P = [1, 2, 3, 4]
    M = [0, -4, -8, -12]
    F = [-1, -6, -11, -16]

    SCORE_MAP = {'R': R, 'P': P, 'M': M, 'F': F}
    CONFIDENCE_TO_INDEX = {25: 0, 50: 1, 75: 2, 100: 3}

    task_df = df[df['question_number'] == question_number].copy()

    def score_row(row):
        alt = int(row['answer_alternative'])
        confidence = int(row['confidence_level'])
        if confidence == 0:
            return 0
        letter = map_answers[alt - 1]
        score_array = SCORE_MAP[letter]
        return score_array[CONFIDENCE_TO_INDEX[confidence]]

    task_df['score'] = task_df.apply(score_row, axis=1)
    return task_df.groupby('student_id', as_index=False)['score'].sum()