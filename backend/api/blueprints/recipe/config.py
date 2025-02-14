import os

class Config:
    """Configuration principale de l'application Flask"""

    # 🔹 Clé secrète (pour sessions, JWT...)
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")

    # 🔹 Connexion à la base de données (Par défaut SQLite, peut être PostgreSQL/MySQL)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔹 CORS (Autorisation des requêtes depuis un front-end)
    CORS_HEADERS = "Content-Type"
    
    # 🔹 Mode Debug (Désactiver en production !)
    DEBUG = True

    # 🔹 Pagination par défaut (ex: afficher 10 recettes par page)
    ITEMS_PER_PAGE = 10
