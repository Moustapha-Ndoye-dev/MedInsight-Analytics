import pandas as pd

def validate_hospital_data(df: pd.DataFrame) -> bool:
    """
    Vérifie la conformité des données du DataFrame hospitalier.
    Lève une erreur (ValueError) si une anomalie est détectée.
    """
    required_columns = ['PatientID', 'Age', 'Sexe', 'Departement', 'Maladie', 'DureeSejour', 'Cout', 'DateAdmission', 'DateSortie', 'Traitement']
    
    # 1. Vérification des colonnes
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Erreur de validation : Colonne manquante -> {col}")
    
    # 2. Vérification des valeurs logiques
    if (df['Age'] < 0).any():
        raise ValueError("Erreur de validation : L'âge ne peut pas être un nombre négatif.")
        
    if (df['DureeSejour'] < 0).any():
        raise ValueError("Erreur de validation : La durée de séjour ne peut pas être négative.")
        
    if (df['Cout'] < 0).any():
        raise ValueError("Erreur de validation : Le coût d'hospitalisation ne peut pas être négatif.")
        
    print("Validation des donnees passee avec succes.")
    return True
