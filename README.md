# 🏥 MedInsight Analytics : Intelligence Exécutive pour le Pilotage Stratégique Hospitalier

![MedInsight Branding](assets/hero.png)

<div align="center">

[![Python Engine](https://img.shields.io/badge/Engine-Python%203.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Analytical Core](https://img.shields.io/badge/Core-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Visualization Layer](https://img.shields.io/badge/Layer-Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Protocol](https://img.shields.io/badge/Protocole-MIT-44CC11?style=for-the-badge)](LICENSE)

</div>

## 🌐 Genèse du Projet
**MedInsight Analytics** est un système de support à la décision de haut niveau, conçu pour structurer les données cliniques et financières en actifs stratégiques. En s'appuyant sur une modélisation statistique avancée et une orchestration de Machine Learning, la plateforme offre aux directions hospitalières un cadre robuste pour l'optimisation de la **Durée Moyenne de Séjour (DMS)** et de l'efficience structurelle.

---

## 📊 Indicateurs de Performance Centraux

| Métrique | Précision | Signification Stratégique |
| :--- | :--- | :--- |
| **Fiabilité du Modèle ($R^2$)** | **81%** | Réduction significative de la variance dans les prévisions budgétaires. |
| **Signal d'Intégrité des Données** | **Optimal** | Isolation automatisée des valeurs aberrantes cliniques pour une modélisation sans biais. |
| **Consistance Analytique** | **Élevée** | Résultats validés de manière croisée sur plusieurs départements hospitaliers. |
| **Interface Exécutive** | **Segoe UI** | Standard visuel Premium pour les rapports de conseil d'administration. |

---

## 🚀 Cadre Analytique Avancé

### 🧠 Orchestration du Machine Learning
Notre pipeline utilise une approche multi-étapes pour garantir la qualité des données et la précision prédictive :
*   **🛡️ Prétraitement Robuste** : Implémentation d'algorithmes **Isolation Forest** pour la détection d'anomalies en haute dimension, garantissant l'élimination des artefacts cliniques et des cas de facturation atypiques.
*   **💶 Modélisation Prédictive des Coûts** : Analyse de régression de haute précision focalisée sur les moteurs de coûts structurels ($R^2=0.81$).
*   **🕒 Dynamique des Flux Opérationnels** : Classification discrète des séjours pour un **Gestion des Lits (Bed Management)** proactif et une planification optimisée des sorties.
*   **👥 Identification de Groupes Latents** : Clustering non supervisé **K-Means** pour identifier les segments de patients à forte variance et optimiser les parcours de soins gériatriques.

### 📈 Excellence Visuelle
*   **Intelligence Dynamique** : Moteur **Plotly** interactif pour une exploration granulaire des données.
*   **Esthétique Institutionnelle** : Thème UI personnalisé basé sur **Segoe UI** pour répondre aux standards institutionnels les plus élevés.
*   **Clarté Décisionnelle** : Tableaux de bord épurés privilégiant l'intelligence actionnable au "bruit" des données brutes.

---

## 📂 Architecture du Système

```text
MedInsight-Analytics/
├── 📁 assets/                  # Branding institutionnel et actifs visuels
├── 📁 data_processing/         # Pipelines de prétraitement et feature engineering
├── 📁 generate_report/         # Moteur de génération de rapports statiques (HTML/Exécutif)
├── 📁 machine_learning/        # Définitions des modèles (Régression, Classification, Clustering)
├── 📁 statistical_analysis/    # Analyses exploratoires (EDA) et études de variance
├── 📁 visualizations/          # Moteur de rendu (Thème Plotly/Segoe)
├── 📁 rapport_html/            # Sortie finale du rapport exécutif
├── 📜 hospital_data.csv        # Jeu de données cliniques et financières primaire
├── 📜 Analyse_Hospitaliere.ipynb # Notebook technique central
└── 📜 requirements.txt         # Dépendances au niveau système
```

---

## 🛠️ Déploiement & Orchestration

### 1. Initialisation de l'Environnement
```bash
# Cloner le coeur analytique
git clone https://github.com/Moustapha-Ndoye-dev/MedInsight-Analytics.git
cd MedInsight-Analytics

# Configuration de l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Résolution des dépendances
pip install -r requirements.txt
```

### 2. Exécution du Pipeline Analytique
Générez le rapport exécutif interactif via notre script de build automatisé :
```bash
python generate_report/notebook_to_rapport.py
```

---

## 💡 Recommandations Stratégiques
Le système identifie trois leviers critiques pour l'optimisation structurelle :
1.  **Gestion Intégrée des Lits** : Alertes de sortie prédictives à T+24h pour fluidifier les transitions vers l'HAD.
2.  **Standardisation des Parcours Cliniques** : Réduction de la variance pour les cohortes 75+ afin de stabiliser les marges départementales.
3.  **Gouvernance Financière Prédictive** : Monitoring automatisé des objectifs de coûts basé sur des référentiels spécifiques par département.

---

### ✍️ Auteur
**Moustapha Ndoye**  
*Analyste Junior en Données Cliniques et Financières*

---

*© 2024 MedInsight Analytics - Architecturer l'Excellence Clinique par la Donnée.*
