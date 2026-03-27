import pandas as pd
import numpy as np

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """Charge et nettoie les données hospitalières."""
    df = pd.read_csv(filepath, sep=';')
    
    # Nettoyage et conversion (si nécessaire)
    if 'DateAdmission' in df.columns:
        df['DateAdmission'] = pd.to_datetime(df['DateAdmission'], format='%Y-%m-%d', errors='coerce')
    if 'DateSortie' in df.columns:
        df['DateSortie'] = pd.to_datetime(df['DateSortie'], format='%Y-%m-%d', errors='coerce')
        
    # Remplir les valeurs manquantes si applicable
    df['Age'] = df['Age'].fillna(df['Age'].median())
    
    return df
