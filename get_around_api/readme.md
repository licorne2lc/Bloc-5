---
title: Get Around Api
emoji: 🌍
colorFrom: green
colorTo: red
sdk: docker
pinned: false
short_description: Prédiction du tarif de location à la journée
---

## 🚀 API GetAround – Location de voiture

Bienvenue sur l'API GetAround ! Cette API permet de prédire le **prix de location journalier** d'une voiture à partir de ses caractéristiques.

---

### ✅ État de fonctionnement de l'espace

- **URL de l’espace** :  
  🔗 [https://huggingface.co/spaces/licorne2lc/get_around_api](https://huggingface.co/spaces/licorne2lc/get_around_api)

- **Message de fonctionnement** :

```json
{
  "message": "Bienvenue sur l'API GET Around! auteur —> Jerome Moulinier",
  "model_status": "✅ Modèle chargé avec succès"
}
```

---

### 📬 Endpoint de prédiction

- **URL de l’interface Swagger (docs)** :  
  📎 [https://licorne2lc-get-around-api.hf.space/docs#/Prediction/predict_predict_post](https://licorne2lc-get-around-api.hf.space/docs#/Prediction/predict_predict_post)

- **Méthode HTTP** : `POST`  
- **Endpoint** : `/predict`

Exemple de payload :

```json
{
  "model_key": "Peugeot",
  "mileage": 13131,
  "engine_power": 110,
  "fuel": "diesel",
  "paint_color": "grey",
  "car_type": "convertible",
  "private_parking_available": true,
  "has_gps": true,
  "has_air_conditioning": true,
  "automatic_car": true,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": true
}
```

---

### 🔧 Stack technique

- Python 3.10
- FastAPI
- scikit-learn (v1.6.1)
- joblib
- Docker (SDK Hugging Face)

---

### 👤 Auteur

Jerome Moulinier – [github.com/licorne2lc](https://github.com/licorne2lc)

---