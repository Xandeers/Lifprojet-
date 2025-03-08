# Lifprojet

## Setup

Deux façons de setup le projet: avec ou sans Docker.

### Avec Docker

Il faut juste Docker d'installé. Il y a pour l'instant le ``compose.dev.yml`` pour setup un environement de developpement.

```bash
docker compose -f compose.dev.yml up -d --build
```

Le ``--build`` est à mettre la première fois ou pour quand on rajoute une bibliothèque, cela permet de reconstruire l'image du projet backend. En dehors de ces cas il est optionnel.

Une fois les 3 containers lancés:
- API dispo sur http://localhost:5000
- pgweb sur http://localhost:8081

On peut avoir besoin d'executer des commandes Python (pour faire des migrations par exemple), dans ce cas on peut lancer un shell sur le container du backend.

```bash
docker exec -it lifprojet_api /bin/bash
flask db upgrade # par exemple
```

**TODO: faut rajouter le frontend dans le compose**

### Manuellement

C'est un peu plus chaud et je te conseille d'avoir un environnement Linux pour éviter les soucis.

### Pré-requis:
- Python 3.12+ (plus vieux ça peut marcher)
- NodeJS 22.14+ (pareil plus vieux ça peut marcher)
- PostgreSQL 17+
- Quelques dépendences

Sur Ubuntu / Debian récent ça donne:

```bash
sudo apt update -y && sudo apt install -y build-essential libpq-dev python3 python3-pip python3-venv python3-dev nodejs postgresql postgresql-client
```

Pour setup l'API:
```bash
cd backend
python3 -m .venv venv
source .venv/bin/activate
pip install --no-cache-dir -r requirements.txt
cp .env.example .env # là tu configure la base de donnée pgsql dans le .env
python3 run.py # pour lancer le serveur de dev
```

ça doit tourner sur http://localhost:5000

Pour setup le frontend:
```bash
cd frontend
npm i
npm run dev
```