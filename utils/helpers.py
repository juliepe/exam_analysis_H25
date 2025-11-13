import binascii
import hashlib
import os #File and directory manipulation
from pathlib import Path
import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Load data from CSV file
    
    Args:
        file_path (str): Path to the CSV file

    Returns:
        pandas.DataFrame: Loaded DataFrame
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        print(f"Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def save_pickle_file(df, name, folder='data'):
    """
    Save a DataFrame to a pickle file.

    Args:
        df (pandas.DataFrame): The DataFrame to save
        name (str): Name for the output pickle file (without extension)
        folder (str or Path): Folder path where the file should be saved (default: 'data')
    """
    # Ensure folder exists
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    # Create full file path
    path = folder / f"{name}.pkl"

    try:
        df.to_pickle(path)
        print(f"✅ DataFrame saved as: {path}")
    except Exception as e:
        print(f"❌ Error saving DataFrame: {e}")


def save_csv_file(df, name, folder='data'):
    """
    Save a DataFrame to a CSV file.

    Args:
        df (pandas.DataFrame): The DataFrame to save
        name (str): Name for the output CSV file (without extension)
        folder (str or Path): Folder path where the file should be saved (default: 'data')
    """
    # Ensure folder exists
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    # Create full file path
    path = folder / f"{name}.csv"

    try:
        df.to_csv(path, index=False)
        print(f"✅ DataFrame saved as: {path}")
    except Exception as e:
        print(f"❌ Error saving DataFrame: {e}")


def derive_irreversible_id(original_id: str, salt: bytes, iterations=200): # standard iterations is 200,000
    """
    Generate irreversible anonymized ID using PBKDF2-HMAC-SHA256.
    
    Args:
        original_id (str): Original identifier to anonymize
        salt (bytes): Random salt for unique hashes
        iterations (int): PBKDF2 iterations (default: 200, standard: 200,000)
    
    Returns:
        str: Hexadecimal hash string
    """
    # PBKDF2-HMAC-SHA256 -> produces derived bytes, then hex
    dk = hashlib.pbkdf2_hmac('sha256', original_id.encode('utf-8'), salt, iterations)
    return binascii.hexlify(dk).decode('ascii')


def anonymize_dataframe_with_salt(df, column_name: str):
    """
    Anonymize DataFrame column by replacing values with irreversible hashes.
    
    Args:
        df (pandas.DataFrame): DataFrame to modify in-place
        column_name (str): Column name to anonymize
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")

    salt = os.urandom(32)             # per-exam random salt, os.urandom generates cryptographically secure random bytes
    df[column_name] = df[column_name].apply(lambda x: derive_irreversible_id(str(x), salt))
    del salt


def anonymize_IDs(df, column_name: str):
    """
    Anonymizing candidate IDs in a DataFrame by changing each id with a random number from 1 to n, 
    where the same random number is assigned to the same candidate ID.

    Args:
        df (pandas.DataFrame): DataFrame to modify in-place
        column_name (str): Column name containing candidate IDs
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")
    
    # Use factorize to get unique identifiers for each unique value
    codes, uniques = pd.factorize(df[column_name])
    
    # Create a random permutation of numbers from 1 to n (where n is number of unique values)
    n_unique = len(uniques)
    random_ids = np.random.permutation(range(1, n_unique + 1))
    
    # Map the factorized codes to random IDs
    df[column_name] = random_ids[codes]


def compare_columns(df, name1:str, name2:str):
    """
    Compare two columns in a DataFrame and return the number of matching entries.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the columns to compare
        name1 (str): Name of the first column
        name2 (str): Name of the second column

    Returns:
        int: Number of matching entries
    """

    try:
        for i in range(len(df)):
            if df[name1][i] != df[name2][i]:
                print(f"Row {i} is different: {df[name1][i]} != {df[name2][i]}")
        print(f"the rows are identical")
    except Exception as e:
        print(f"❌ One or both of the columns are not found: {e}")