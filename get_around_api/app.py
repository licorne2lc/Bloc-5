import uvicorn
import pandas as pd 
from pydantic import BaseModel
from fastapi import FastAPI
from joblib import load
import os

description = """
API GetAround – conçue pour vous aider à prédire le prix de location de votre voiture !
Voici les points d’accès disponibles :

/ : Cet endpoint permet d’explorer la fonctionnalité de prédiction.

/predict : Cet endpoint accepte une requête POST avec des données JSON en entrée. Vous pouvez l’utiliser pour effectuer des prédictions en fournissant les informations nécessaires sur votre voiture.

N’hésitez pas à utiliser l’endpoint /predict en envoyant une requête POST avec les données JSON requises pour obtenir une estimation précise du prix de location de votre véhicule.
"""

tags_metadata = [
    {
        "name": "Simple Endpoint",
        "description": "Simple endpoint to try out!",
    },
    {
        "name": "Prediction",
        "description": "Prediction of the rental price based"
    }
]

app = FastAPI(
    title="🚙 GetAround price prediction ",
    description=description,
    version="1.0",
    openapi_tags=tags_metadata,
)

# ✅ Vérification du chargement du modèle
model = None
model_status = "❌ Modèle non chargé"

try:
    model = load("model.joblib")
    model_status = "✅ Modèle chargé avec succès"
except Exception as e:
    model_status = f"❌ Erreur de chargement du modèle : {e}"


# Data types for prediction
class PredictionFeatures(BaseModel):
    model_key: str = "Peugeot"
    mileage: int = 13131
    engine_power: int = 110
    fuel: str = "diesel"
    paint_color: str = "grey"
    car_type: str = "convertible"
    private_parking_available: bool = True
    has_gps: bool = True
    has_air_conditioning: bool = True
    automatic_car: bool = True
    has_getaround_connect: bool = True
    has_speed_regulator: bool = True
    winter_tires: bool = True

@app.get("/", tags=["Simple Endpoint"])
def index():
    return {
        "message": "Bienvenue sur l'API GET Around! auteur —> Jerome Moulinier",
        "model_status": model_status
    }

@app.post("/predict", tags=["Prediction"])
async def predict(features: PredictionFeatures):
    try:
        # Convertir en DataFrame
        information = pd.DataFrame([features.dict()])
        
        # Prédiction
        prediction = model.predict(information)

        # Résultat arrondi à 2 décimales
        return {"prediction": round(prediction.tolist()[0], 2)}

    except Exception as e:
        return {
            "error": str(e),
            "columns_received": list(information.columns),
            "example_data": information.to_dict(orient="records")[0]
        }



if __name__ == "__main__":
    
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
