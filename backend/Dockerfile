FROM python:3.12-slim

# Empêche Python d’écrire des .pyc + force stdout/stderr immédiat + optimise pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# dépendances python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le projet (en dev on monte le volume, mais on garde cette copie
# pour pouvoir build une image standalone si besoin)
COPY . /app

# ⚠️ NOTE: En production, on utiliserait un build multi-stage (wheel builder)
# et un serveur WSGI (ex: gunicorn/uvicorn) au lieu de runserver pour optimiser
# la taille de l’image et la robustesse du runtime.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]