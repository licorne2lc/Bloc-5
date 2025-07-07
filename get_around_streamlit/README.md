---
title: Getaround Streamlit Dashboard
emoji: 🚗
colorFrom: pink
colorTo: indigo
sdk: docker
pinned: false
app_port: 8501
---

# 🚗 Dashboard Getaround

Bienvenue sur le tableau de bord interactif **Getaround** !

Ce dashboard Streamlit vous permet de :

### 📊 Analyses exploratoires (EDA)
- Explorer les **retards de location** et leur gravité.
- Visualiser l’impact des retards sur la **réservation suivante**.
- Analyser la **répartition des check-ins** et des états de location.
- Étudier la **distribution des prix** selon :
  - le type de voiture 🚙
  - le carburant ⛽
  - la présence de Getaround Connect 🔗
  - la puissance moteur ⚙️

### 🔮 Prédiction du prix
- Un formulaire intelligent permet d’estimer le prix journalier d’une voiture à partir de ses caractéristiques.
- L’estimation est faite via une API déployée dans un [Space Hugging Face dédié](https://huggingface.co/spaces/licorne2lc/get_around_api).

### 📎 Liens utiles
- 🔌 API utilisée pour les prédictions : [Voir la documentation Swagger](https://licorne2lc-get-around-api.hf.space/docs)
- 🧠 Notebook d’analyse : inclus dans la version locale

---

**Technologies** :
- Streamlit
- Plotly
- Seaborn & Matplotlib
- API REST (FastAPI)
- Docker

---

**Auteur** : [licorne2lc](https://huggingface.co/licorne2lc) • Projet encadré par Jedha Bootcamp
