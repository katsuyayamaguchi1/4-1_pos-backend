# db_control/insert_test_data.py

from sqlalchemy.orm import sessionmaker
from mymodels_MySQL import ProductMaster
from connect_MySQL import engine

def insert_products():
    Session = sessionmaker(bind=engine)
    session = Session()

    # 登録したい文房具のリスト
    stationery_products = [
        ProductMaster(CODE="1", NAME="テクワンロゴ入りのペン", PRICE=300),
        ProductMaster(CODE="2", NAME="何でも消える消しゴム", PRICE=1400000),
        ProductMaster(CODE="3", NAME="書いたことが実現するノート", PRICE=12000000),
    ]

    try:
        print("🟡 文房具のテストデータを登録しています...")
        session.add_all(stationery_products)
        session.commit()
        print("✅ テストデータの登録が完了しました。")
    except Exception as e:
        print(f"❌ 登録中にエラーが発生しました: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    insert_products()