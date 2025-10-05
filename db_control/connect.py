from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# db_control フォルダ内にある CRM.db を指定
DB_PATH = os.path.join(os.path.dirname(__file__), "CRM.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# SQLite は check_same_thread=False を付ける
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True  # ← SQLログを出したければ残してOK
)

# SessionLocal を必ず定義（これが必要）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
