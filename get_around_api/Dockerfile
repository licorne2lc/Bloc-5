# Image officielle, légère et maintenue
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /home/app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l’application
COPY . .

# Définir la variable d’environnement pour Hugging Face
ENV PORT=7860

# Lancer le serveur avec Gunicorn + Uvicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--worker-class", "uvicorn.workers.UvicornWorker"]