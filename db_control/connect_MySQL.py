from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from pathlib import Path # pathlibをインポートして、パスを安全に扱います

# 環境変数の読み込み
load_dotenv()

# --- SSL証明書の絶対パスを自動的に見つける ---
# このファイル(connect_MySQL.py)の場所を基準にします
# Path(__file__).parent -> このファイルがあるフォルダ (db_control)
# ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# 証明書は 'db_control' フォルダの中にあるため、.parentは1回でOKです
# ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
DB_CONTROL_DIR = Path(__file__).parent
# db_controlフォルダのパスと証明書のファイル名を結合して、絶対パスを作成します
CERT_FILE_PATH = DB_CONTROL_DIR / "DigiCertGlobalRootG2.crt.pem"

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    echo=True, # SQLをコンソールに表示する設定
    connect_args={
        # 自動で見つけた証明書の絶対パスを使う
        "ssl_ca": str(CERT_FILE_PATH)
    }
)