FROM python:3.11-slim


# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip + installer setuptools et wheel
RUN pip install --upgrade pip setuptools wheel

# Créer un dossier de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt ./
COPY app.py ./
COPY get_around_delay_analysis.xlsx ./
COPY get_around_pricing_project.csv ./
COPY logo.png ./

# Installer les dépendances Python (avec wheels)
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 7860

# Lancer Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

