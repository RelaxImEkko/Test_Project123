from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

print("==== DATABASE_URL ====")
print(settings.DATABASE_URL)
print("======================")

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
