# Fullstack Movies App

Application fullstack de gestion de films, acteurs et critiques.  
Stack : Django + DRF (backend), Vue 3 + Vuetify + Pinia (frontend), Docker Compose.

## 🚀 Démarrage rapide

```bash
# 1. Cloner le repo
git clone https://github.com/RAFFENNEvalentin/fullstack-movies.git
cd fullstack-movies

# 2. Copier la configuration
cp .env.sample .env

# 3. Lancer l'application
docker compose up --build

# 4. Initialiser la base de données
docker compose exec backend python manage.py migrate

# 5. (Optionnel) Créer un super utilisateur pour /admin
docker compose exec backend python manage.py createsuperuser

# 6. Lancer les tests backend
docker compose exec backend python manage.py test -v 2

#FYI
URLs utiles
	•	API root : http://localhost:8000/api/
	•	API healthcheck : http://localhost:8000/api/health/
	•	Admin Django : http://localhost:8000/admin
	•	Docs API (Swagger) : http://localhost:8000/api/docs/
	•	OpenAPI schema JSON : http://localhost:8000/api/schema/