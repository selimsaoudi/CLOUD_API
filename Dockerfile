FROM python:3.11-slim

# Dossier de travail dans l'image
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY server.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer FastAPI sur le port 8000
EXPOSE 8000

# Commande pour lancer l’API
CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]