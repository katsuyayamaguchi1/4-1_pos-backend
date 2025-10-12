# db_control/connect_MySQL.py
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from pathlib import Path

# .env 読み込み
load_dotenv()

# ドライバ切替（sqlite / mysql）
DB_DRIVER = os.getenv("DB_DRIVER", "mysql").lower()

if DB_DRIVER == "sqlite":
    # ---- SQLite（ローカルファイル）----
    # プロジェクト直下に local.db を作成します
    DATABASE_URL = "sqlite:///./local.db"
    engine = create_engine(DATABASE_URL, echo=True)
else:
    # ---- MySQL（従来どおり）----
    DB_CONTROL_DIR = Path(__file__).parent
    CERT_FILE_PATH = DB_CONTROL_DIR / "DigiCertGlobalRootG2.crt.pem"

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    engine = create_engine(
        DATABASE_URL,
        echo=True,  # SQLログ表示
        connect_args={"ssl_ca": str(CERT_FILE_PATH)},
    )
