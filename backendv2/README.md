# Backend

Cette partie contient l'API du site, elle est écrite en Python avec FastAPI et utilise un SGBD PostgreSQL.

## Installation

1) Pour mettre en place la BDD facilement, il est conseillé d'utiliser Docker + Docker Compose.
```bash
docker compose up -d 
```

- Le SGBD écoutera sur **localhost:5432**
- Une BDD par défaut **api_db** est crée avec les identifiants **api** / **api**
- un panel pgWeb est disponible sur http://127.0.0.1:8081

2) Pour mettre en place l'API il est nécessaire d'avoir **Python 3.12+** et [**uv (gestionnaire de dépendences)**](https://github.com/astral-sh/uv) d'installé sur sa machine
   (sachant que UV gère aussi l'installation de Python au besoin c'est comme vous voulez)

3) Créer le fichier **.env** à partir du **.env.example** (les données par défaut sont déjà correctes)
4) Installation des dépendences avec **uv**
```bash
uv sync # installe les dépendences
```

5) Effectuer les migrations pour créer les tables:
```bash
uv run alembic upgrade head
```

6) Lancer le serveur de développement
```bash
uv run fastapi run
```

- Il tourne sur http://127.0.0.1:8000 
- La documentation Swagger est accessible sur http://127.0.0.1:8000/docs

## Dataset

- Le projet propose un script pour peupler la table **products** avec le dataset Ciqual, vous pouvez l'executer avec:

```bash
uv run -m app.cli import-ciqual
```

- Le projet propose aussi un script pour remplir la table **recipes** avec des recettes générées par GPT de OpenAI.
Il faut renseigner sa clé dans le **.env** et avoir un peu de crédit, j'utilise le modèle **gpt-3.5-turbo** 
qui est pas cher et fonctionne bien avec le bon prompt mais il manque de créativité tout de même...

__Note: Il faut que les idéntifiants du faker dans le .env correspondent à un vrai compte inscrit__

```bash
uv run -m app.cli fake-recipes [nbr de recettes] [optionnel: URL de miniature par défaut rien]
```