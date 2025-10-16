#以下、STEP4-1level1ベース

# create_tables_MySQL.py

# 同じフォルダにあるファイルをインポートするので、フォルダ名は不要
from mymodels_MySQL import Base
from connect_MySQL import engine

def create_pos_tables():
    """
    POSアプリケーションに必要なテーブルをデータベースに作成します。
    """
    try:
        print("POSアプリ用のテーブルをAzure Database for MySQLに作成します...")
        Base.metadata.create_all(bind=engine)
        print("テーブルの作成が完了しました。")
    except Exception as e:
        print(f"作成中にエラーが発生しました: {e}")

if __name__ == "__main__":
    create_pos_tables()



# 以下、STEP3ベース

# インポートするクラス名を 'Customer' (単数形) に修正します
# from db_control.mymodels_MySQL import Base, Customer
# from db_control.connect_MySQL import engine

# def create_database():
#     try:
#         print("Azure Database for MySQLにテーブルを作成します...")
#         Base.metadata.create_all(bind=engine)
#         print("作成が完了しました。")
#     except Exception as e:
#         print(f"作成中にエラーが発生しました: {e}")

# if __name__ == "__main__":
#     create_database()
