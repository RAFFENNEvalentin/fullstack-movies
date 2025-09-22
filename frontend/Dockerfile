FROM node:20-alpine

WORKDIR /app

# install deps (on aura le package.json quand on init le front)
COPY package*.json ./
RUN npm install

# sources (montés en volume en dev, mais on copie pour build propre si besoin)
COPY . .

EXPOSE 5173

# ⚠️ NOTE: En production, on ne lancerait pas le serveur Vite en mode dev.
# On ferait plutôt un `npm run build` pour générer des fichiers statiques,
# puis on les servirait via un serveur optimisé (ex: Nginx ou un CDN).
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]