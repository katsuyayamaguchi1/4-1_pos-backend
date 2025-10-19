# db_control/create_tables_MySQL.py

from mymodels_MySQL import Base
from connect_MySQL import engine

def recreate_database():
    """
    古いテーブルをすべて削除し、新しい定義で再作成する
    """
    try:
        print("--- データベースの再作成を開始します ---")
        
        # 1. まず、古いテーブルをすべて削除します
        print("🟡 1. 古いテーブルをすべて削除しています...")
        Base.metadata.drop_all(bind=engine)
        print("✅ 1. テーブルの削除が完了しました。")

        # 2. 次に、新しいテーブルを作成します
        print("🟡 2. Lv2用の新しいテーブルを作成しています...")
        Base.metadata.create_all(bind=engine)
        print("✅ 2. テーブルの作成が完了しました。")
        
        print("\n🎉 --- データベースの再作成が完了しました --- 🎉")

    except Exception as e:
        print(f"❌ 再作成中にエラーが発生しました: {e}")

if __name__ == "__main__":
    recreate_database()



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
