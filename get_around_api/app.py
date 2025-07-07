import uvicorn
import pandas as pd 
from pydantic import BaseModel
from fastapi import FastAPI
from joblib import load
import os

description = """
GetAround API, designed to assist you in predicting the rental price for your car!
Here are the available endpoints:
* `/`: This endpoint is provided to explore the predict functionality.
* `/predict`: This endpoint accepts a POST request with JSON input data. You can use this endpoint to make predictions by providing the necessary information about your car.
Feel free to use the `/predict` endpoint by sending a POST request with the required JSON data to obtain accurate rental price predictions for your vehicule
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