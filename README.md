# bloc-5
Deploiement - Projjet Get Around

# Getaround - Analyse, Prédiction et Dashboard

Ce projet vise à analyser les données de location de voitures issues de la plateforme **Getaround**, à créer un modèle de prédiction de prix, et à déployer un tableau de bord interactif ainsi qu'une API REST.

## Auteurs

Projet réalisé par Jerome Moulinier dans le cadre de la certification du bloc 5 **Full Stack Data - Jedha Bootcamp**.

---

## 1. Analyse Exploratoire des Données (EDA)

À partir du fichier Excel `get_around_delay_analysis.xlsx`, plusieurs analyses ont été réalisées :

- **Répartition des types de check-in**
- **États des locations** (`ended` vs `canceled`)
- **Analyse des retards** :
  - Catégorisation des retards (avance / à l’heure / en retard)
  - Gravité des retards (par durée)
  - Impact des retards sur la réservation suivante

Un second fichier CSV `get_around_pricing_project.csv` a permis d'analyser :

- **Répartition des prix journaliers**
- **Influence des caractéristiques du véhicule** sur le prix :
  - Type de carburant
  - Type de voiture
  - Présence de Getaround Connect
  - Puissance moteur

---

## 2. Modèle de Machine Learning

Un **modèle de régression** a été entraîné pour prédire le prix journalier d’un véhicule à partir de ses caractéristiques :

- **Variables utilisées** : mileage, engine_power, fuel, car_type, etc.
- Le modèle a été exporté et intégré dans une API FastAPI déployée sur Hugging Face.

---

## 3. API de Prédiction

L’API permet de soumettre les caractéristiques d’un véhicule et retourne une estimation du **prix de location journalier**.

- Etat du service api prediction Hugging Face :  
  🔗 [https://huggingface.co/spaces/licorne2lc/get_around_api](https://huggingface.co/spaces/licorne2lc/get_around_api)
      le message de disponibilité du service doit apparaitre:
      {"message":"Bienvenue sur l'API GET Around! auteur —> Jerome Moulinier","model_status":"✅ Modèle chargé avec succès"}


-  End point predict disponible a l'url:  
  🔗 [https://licorne2lc-get-around-api.hf.space/docs#/Prediction/predict_predict_post](https://licorne2lc-get-around-api.hf.space/docs#/Prediction/predict_predict_post) --> request swagger en post sur l'endpoint 
---

## 4. Dashboard interactif (Streamlit)

Le tableau de bord est déployé via Streamlit dans un Espace Hugging Face :

🔗 [https://huggingface.co/spaces/licorne2lc/get_around_streamlit](https://huggingface.co/spaces/licorne2lc/get_around_streamlit)

###  Options disponibles dans la sidebar :

1. ** EDA Delay**  
   Analyse des retards, types de check-in, gravité des retards, impact sur les annulations.

2. ** EDA Pricing**  
   Visualisation des facteurs influençant le prix journalier : carburant, voiture, connectivité, puissance moteur...

3. ** Simulation seuil entre location**  
   Outil d’aide à la décision pour fixer un **délai minimum entre deux locations successives** :

   - Calcule le pourcentage de **locations incompatibles** selon le seuil sélectionné (en tenant compte du retard réel des précédentes locations).
   - Affiche également le pourcentage de **retards absorbés** par ce seuil.
        
4. ** API Prediction**  
   Formulaire pour envoyer les caractéristiques d’un véhicule et afficher la **prédiction du prix** retournée par l’API.

5. **👉 Deux liens utiles permettent également de **vérifier la disponibilité des services API** dans la sidebar du dashboard :
-  Espace API HuggingFace
-  Docs API /predict

---

##  Outils utilisés

- Python 3.11
- Pandas, Seaborn, Plotly
- Scikit-learn
- FastAPI
- Streamlit
- Docker
- Git LFS
- Hugging Face Spaces

---

