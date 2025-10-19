# db_control/connect_MySQL.py
import os
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from dotenv import load_dotenv

# ① .env を最優先でロード（OS環境変数より .env を優先）
load_dotenv(override=True)

DB_DRIVER = (os.getenv("DB_DRIVER") or "mysql").lower()

if DB_DRIVER == "sqlite":
    DATABASE_URL = "sqlite:///./local.db"
    engine = create_engine(DATABASE_URL, echo=True)
else:
    # ② 環境変数を取得（None/空/空白を潰す）
    DB_USER = (os.getenv('DB_USER') or "").strip()
    DB_PASSWORD = (os.getenv('DB_PASSWORD') or "").strip()
    DB_HOST = (os.getenv('DB_HOST') or "").strip()
    DB_PORT = (os.getenv('DB_PORT') or "").strip()
    DB_NAME = (os.getenv('DB_NAME') or "").strip()

    # ③ "None" / 空なら 3306 に補正（ここが今回の肝）
    if not DB_PORT or DB_PORT.lower() == "none":
        DB_PORT = "3306"

    # ④ URLエンコード（記号入りパスワード対策）
    user = quote_plus(DB_USER)
    pwd  = quote_plus(DB_PASSWORD)

    # ⑤ SSL証明書（存在する場合のみ渡す：無くても動きます）
    CERT_FILE_PATH = Path(__file__).parent / "DigiCertGlobalRootG2.crt.pem"
    connect_args = {}
    if CERT_FILE_PATH.exists():
        connect_args["ssl_ca"] = str(CERT_FILE_PATH)

    # ⑥ PyMySQL を利用（requirements に PyMySQL は入っています）
    DATABASE_URL = f"mysql+pymysql://{user}:{pwd}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

    # デバッグ出力（機微情報は出さない）
    print(f"[DB] host={DB_HOST} port={DB_PORT} user={DB_USER} name={DB_NAME} ssl_ca={CERT_FILE_PATH.exists()}")

    engine = create_engine(
        DATABASE_URL,
        echo=True,          # 必要に応じて False
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args=connect_args,
    )
