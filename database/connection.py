from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_HOST = 'localhost'
DB_PORT = 330
DB_USER = 'root'
DB_PASSWORD = '***********'
DB_NAME = 'db_admin_portal'


DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_engine():
    return engine


def get_session():
    return SessionLocal()
