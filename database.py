from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Informations de connexion à MySQL via XAMPP
DB_USER = "root"
DB_PASSWORD = ""  # vide par défaut sur XAMPP
DB_HOST = "127.0.0.1"
DB_NAME = "focusclass"

# URL de connexion SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Création du moteur
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()
