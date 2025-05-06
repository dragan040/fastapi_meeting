from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 👉 REMPLACE les valeurs ci-dessous par celles de Railway (onglet Variables)
DB_USER = "root"  # ou le nom d'utilisateur Railway (MYSQLUSER)
DB_PASSWORD = "HRFBXWUjamSgwYHXHYSBkvQGuWnUjCHL"  # MYSQLPASSWORD
DB_HOST = "mysql.railway.internal"  # MYSQLHOST
DB_PORT = "3306"  # généralement 3306
DB_NAME = "railway"  # MYSQLDATABASE

# 🚀 URL de connexion complète
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 🔧 Configuration SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
