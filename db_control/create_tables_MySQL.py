# インポートするクラス名を 'Customer' (単数形) に修正します
from db_control.mymodels_MySQL import Base, Customer
from db_control.connect_MySQL import engine

def create_database():
    try:
        print("Azure Database for MySQLにテーブルを作成します...")
        Base.metadata.create_all(bind=engine)
        print("作成が完了しました。")
    except Exception as e:
        print(f"作成中にエラーが発生しました: {e}")

if __name__ == "__main__":
    create_database()
