# db_control/check_data.py

from sqlalchemy.orm import sessionmaker
# ↓↓↓【修正点】先頭のドット(.)を削除 ↓↓↓
from mymodels_MySQL import ProductMaster
from connect_MySQL import engine
# ↑↑↑【修正点】先頭のドット(.)を削除 ↑↑↑

def check_product_data():
    # (関数の内容は変更なし)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        products = session.query(ProductMaster).all()
        if not products:
            print("🔵 product_masterテーブルは空です。")
        else:
            print("🟢 product_masterテーブルに以下のデータがあります：")
            for p in products:
                print(f"  CODE: {p.CODE}, NAME: {p.NAME}, PRICE: {p.PRICE}")
    except Exception as e:
        print(f"❌ データの確認中にエラーが発生しました: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_product_data()