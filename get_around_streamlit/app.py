
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# ========== CONFIGURATION ==========
st.set_page_config(page_title="Getaround Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>🚗 Getaround Dashboard</h1>", unsafe_allow_html=True)

# ========== LOGO ==========
try:
    logo = Image.open("logo.png")
    st.sidebar.image(logo, width=200)
except Exception:
    st.sidebar.warning("Logo non chargé")

# ========== MENU ==========
with st.sidebar:
    selected = option_menu(
        "Menu principal",
        ["🏁 EDA delay", "📈 EDA pricing", "🔮 API prediction"],
        icons=["hourglass-split", "bar-chart-line", "cpu"],
        menu_icon="cast",
        default_index=0,
    )
    st.markdown("---")
    st.markdown("📄 [Espace API HuggingFace](https://huggingface.co/spaces/licorne2lc/get_around_api)")
    st.markdown("🛠️ [Docs API /predict](https://licorne2lc-get-around-api.hf.space/docs)")

# ========== 1. EDA DELAY ==========
if selected == "🏁 EDA delay":
    st.title("📊 Analyse des retards de Getaround")
    try:
        dataset = pd.read_excel("get_around_delay_analysis.xlsx")

        dataset["delay_status"] = dataset["delay_at_checkout_in_minutes"].apply(
            lambda x: "En avance" if x < 0 else "À l’heure" if x == 0 else "En retard"
        )

        def catégoriser_retard(x):
            if x <= 0:
                return "Pas de retard"
            elif x <= 30:
                return "< 30 min"
            elif x <= 60:
                return "30-60 min"
            elif x <= 120:
                return "1h-2h"
            elif x <= 240:
                return "2h-4h"
            else:
                return "> 4h"

        retard_order = ["Pas de retard", "< 30 min", "30-60 min", "1h-2h", "2h-4h", "> 4h"]
        dataset["retard_cat"] = dataset["delay_at_checkout_in_minutes"].apply(catégoriser_retard)
        dataset["retard_cat"] = pd.Categorical(dataset["retard_cat"], categories=retard_order, ordered=True)

        fig_checkin = px.pie(dataset, names="checkin_type", title="Répartition des types de check-in",
                             hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel, width=1000, height=400)
        st.plotly_chart(fig_checkin)

        fig_state = px.pie(dataset, names="state", title="Répartition des états de location",
                           hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3, width=1000, height=400)
        st.plotly_chart(fig_state)

        fig_delay_status = px.pie(dataset, names="delay_status", title="Retards : avance / à l’heure / en retard",
                                  hole=0.4, color_discrete_sequence=px.colors.qualitative.Vivid, width=1000, height=400)
        st.plotly_chart(fig_delay_status)

        filtered = dataset[(dataset["delay_at_checkout_in_minutes"] > 0) & (dataset["delay_at_checkout_in_minutes"] <= 1440)]
        fig_delay_hist = px.histogram(filtered, x="delay_at_checkout_in_minutes", nbins=50,
                                      title="Distribution des retards (0 à 1440 minutes)", width=1000, height=400)
        st.plotly_chart(fig_delay_hist)

        fig_retard_cat = px.bar(dataset["retard_cat"].value_counts().reindex(retard_order),
                                title="Gravité des retards", labels={"value": "Nombre", "index": "Catégorie"},
                                width=1000, height=400)
        st.plotly_chart(fig_retard_cat)

        dataset_for_join_B = dataset[["rental_id", "delay_at_checkout_in_minutes"]].rename(
            columns={"rental_id": "rental_id_join", "delay_at_checkout_in_minutes": "delay_at_checkout_in_minutes_join"}
        )
        dataset_join = pd.merge(dataset, dataset_for_join_B,
                                left_on="previous_ended_rental_id", right_on="rental_id_join")
        dataset_join["real_delay"] = dataset_join["time_delta_with_previous_rental_in_minutes"] - dataset_join["delay_at_checkout_in_minutes_join"]
        dataset_join_clean = dataset_join.dropna(subset=["delay_at_checkout_in_minutes_join"])
        dataset_join_clean["annulation_due_au_retard"] = dataset_join_clean.apply(
            lambda row: "Oui" if row["state"] == "canceled" and row["real_delay"] < 0 else
                        "Annulée (autre raison)" if row["state"] == "canceled" else "Non", axis=1
        )
        fig_annul = px.pie(dataset_join_clean, names="annulation_due_au_retard",
                           title="Répartition des annulations dues au retard du locataire précédent",
                           hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold, width=1000, height=400)
        st.plotly_chart(fig_annul)

    except FileNotFoundError:
        st.error("❌ Fichier Excel non trouvé : get_around_delay_analysis.xlsx")

# ========== 2. EDA PRICING ==========
elif selected == "📈 EDA pricing":
    st.title("💰 Analyse des prix de location Getaround")
    try:
        df_price = pd.read_csv("get_around_pricing_project.csv")

        st.subheader("Distribution du prix journalier")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(df_price["rental_price_per_day"], bins=50, kde=True, ax=ax)
        st.pyplot(fig)

        st.subheader("Prix par type de carburant")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.boxplot(x="fuel", y="rental_price_per_day", data=df_price, ax=ax)
        st.pyplot(fig)

        st.subheader("Prix par type de voiture")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.boxplot(x="car_type", y="rental_price_per_day", data=df_price, ax=ax)
        st.pyplot(fig)

        st.subheader("Prix selon la présence de Getaround Connect")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.boxplot(x="has_getaround_connect", y="rental_price_per_day", data=df_price, ax=ax)
        st.pyplot(fig)

        st.subheader("Corrélation entre puissance moteur et prix journalier")
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.scatterplot(x="engine_power", y="rental_price_per_day", data=df_price, hue="car_type", ax=ax)
        st.pyplot(fig)
    except FileNotFoundError:
        st.error("❌ Fichier CSV non trouvé : get_around_pricing_project.csv")

# ========== 3. API PREDICTION ==========
elif selected == "🔮 API prediction":
    st.title("🔮 Prédiction du prix de location")
    st.markdown("Remplis les informations suivantes pour obtenir une estimation du prix")

    with st.form("prediction_form"):
        model_key = st.selectbox("Modèle de voiture", ["Peugeot", "Audi", "BMW"])
        mileage = st.number_input("Kilométrage", value=50000)
        engine_power = st.number_input("Puissance moteur", value=100)
        fuel = st.selectbox("Type de carburant", ["diesel", "petrol", "electric", "hybrid"])
        paint_color = st.selectbox("Couleur", ["black", "white", "grey", "blue", "red"])
        car_type = st.selectbox("Type de voiture", ["sedan", "convertible", "suv", "coupe"])
        private_parking_available = st.checkbox("Parking privé disponible", value=True)
        has_gps = st.checkbox("GPS", value=True)
        has_air_conditioning = st.checkbox("Climatisation", value=True)
        automatic_car = st.checkbox("Boîte automatique", value=True)
        has_getaround_connect = st.checkbox("Getaround Connect", value=True)
        has_speed_regulator = st.checkbox("Régulateur de vitesse", value=True)
        winter_tires = st.checkbox("Pneus hiver", value=True)
        submitted = st.form_submit_button("📤 Envoyer")

    if submitted:
        data = {
            "model_key": model_key,
            "mileage": mileage,
            "engine_power": engine_power,
            "fuel": fuel,
            "paint_color": paint_color,
            "car_type": car_type,
            "private_parking_available": private_parking_available,
            "has_gps": has_gps,
            "has_air_conditioning": has_air_conditioning,
            "automatic_car": automatic_car,
            "has_getaround_connect": has_getaround_connect,
            "has_speed_regulator": has_speed_regulator,
            "winter_tires": winter_tires,
        }
        api_url = "https://licorne2lc-get-around-api.hf.space/predict"
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                price = round(response.json()["prediction"], 2)
                st.success(f"💰 Prix de location estimé : {price} € / jour")
            else:
                st.error(f"❌ Erreur {response.status_code} : {response.text}")
        except Exception as e:
            st.error(f"❌ Erreur lors de la requête : {e}")
