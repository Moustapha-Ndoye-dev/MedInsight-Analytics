import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, silhouette_score

def remove_anomalies_isolation_forest(df):
    """Détecte et supprime les anomalies en utilisant Isolation Forest."""
    # On isole les variables numériques pertinentes pour la détection
    numeric_cols = ['Age', 'DureeSejour', 'Cout']
    X_num = df[numeric_cols].fillna(0)
    
    # On configure l'Isolation Forest (on estime arbitrairement à 5% le taux de valeurs aberrantes)
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    outlier_labels = iso_forest.fit_predict(X_num)
    
    # 1 pour inliers (normaux), -1 pour outliers (anomalies)
    df_clean = df[outlier_labels == 1].copy()
    nb_outliers = len(df) - len(df_clean)
    
    print(f"🌲 Isolation Forest : {nb_outliers} anomalies/outliers détectées et retirées (sur {len(df)} patients).")
    return df_clean

def prepare_data_for_regression(df):
    """Prépare les données pour la prédiction du coût (Régression)."""
    features = ['Age', 'Sexe', 'Departement', 'Maladie', 'Traitement', 'DureeSejour']
    X = df[features]
    y = df['Cout']
    
    # Encodage One-Hot pour les variables catégorielles
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    # Séparation train/test (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    return (X_train, X_test, y_train, y_test), X_encoded, y

def prepare_data_for_classification(df):
    """Prépare les données pour la classification des séjours longs (> moyenne)."""
    # Création de la variable cible
    # On utilise un seuil plus stratégique : le 75ème percentile pour identifier les séjours VRAIMENT longs
    seuil_long = df['DureeSejour'].quantile(0.75)
    df['SejourLong'] = (df['DureeSejour'] >= seuil_long).astype(int)
    
    features = ['Age', 'Sexe', 'Departement', 'Maladie', 'Traitement']
    X = df[features]
    y = df['SejourLong']
    
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    # Séparation avant scaling pour éviter le data leakage
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    
    # Scaling des variables numériques (Age est la seule ici avant encoding)
    # Pour simplifier, on scale tout le X_encoded
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"⏱️ Seuil séjour long (Q3) : {seuil_long:.2f} jours. Cible 'SejourLong' créée.")
    return (X_train_scaled, X_test_scaled, y_train, y_test), X_encoded, y

def cross_validate_models(X, y):
    """Évalue les modèles par validation croisée à K=5 plis (Cross-Validation)."""
    models = {
        'Régression Linéaire': LinearRegression(),
        'Random Forest': RandomForestRegressor(random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42)
    }
    
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = []
    
    for name, model in models.items():
        # Calcul du R2 moyen sur 5 plis
        r2_scores = cross_val_score(model, X, y, cv=kf, scoring='r2')
        # Calcul du RMSE moyen sur 5 plis (scikit-learn retourne le RMSE en négatif pour maximiser, on inverse)
        rmse_scores = -cross_val_score(model, X, y, cv=kf, scoring='neg_root_mean_squared_error')
        
        cv_results.append({
            'Modèle': name, 
            'CV R² M': round(r2_scores.mean(), 4),
            'CV R² Ecart-Type': f"±{round(r2_scores.std(), 4)}",
            'CV RMSE Moyen': round(rmse_scores.mean(), 2)
        })
        
    cv_df = pd.DataFrame(cv_results).sort_values(by='CV R² M', ascending=False)
    # Renommer la col pour correspondre au format styling R² par la suite
    cv_df.rename(columns={'CV R² M': 'R²'}, inplace=True) 
    return cv_df

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Entraîne et évalue plusieurs modèles de régression sur Test simple."""
    models = {
        'Régression Linéaire': LinearRegression(),
        'Random Forest': RandomForestRegressor(random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42)
    }
    
    results = []
    trained_models = {}
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        results.append({'Modèle': name, 'MAE': round(mae, 2), 'RMSE': round(rmse, 2), 'R²': round(r2, 4)})
        trained_models[name] = model
        
    results_df = pd.DataFrame(results).sort_values(by='R²', ascending=False)
    return results_df, trained_models

def train_classification_models(X_train, X_test, y_train, y_test):
    """Entraîne et évalue plusieurs modèles de classification."""
    models = {
        'Régression Logistique': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42),
        'Arbre de Décision': DecisionTreeClassifier(random_state=42)
    }
    
    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        results.append({
            'Modèle': name,
            'Accuracy': accuracy_score(y_test, preds),
            'Precision': precision_score(y_test, preds, zero_division=0),
            'Recall': recall_score(y_test, preds, zero_division=0),
            'F1-Score': f1_score(y_test, preds, zero_division=0)
        })
        
    return pd.DataFrame(results).sort_values(by='F1-Score', ascending=False)

def get_feature_importance(model, feature_names):
    """Extrait l'importance des variables d'un modèle ensembliste."""
    if hasattr(model, 'feature_importances_'):
        return pd.DataFrame({
            'Feature': feature_names, 
            'Importance': model.feature_importances_
        }).sort_values(by='Importance', ascending=False)
    return None

def perform_patient_clustering(df, n_clusters=3):
    """Groupe les patients par profils de consommation (Âge, Durée, Coût)."""
    features = ['Age', 'DureeSejour', 'Cout']
    X = df[features].fillna(0)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    score = silhouette_score(X_scaled, df['Cluster'])
    print(f"🧬 Clustering effectué : {n_clusters} profils identifiés. Silhouette Score: {score:.3f}")
    
    return df, kmeans
