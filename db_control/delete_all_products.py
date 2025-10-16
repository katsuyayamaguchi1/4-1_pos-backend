# db_control/delete_all_products.py

from sqlalchemy.orm import sessionmaker
from mymodels_MySQL import ProductMaster
from connect_MySQL import engine

def delete_all():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        print("🟡 全ての商品データを削除しています...")
        session.query(ProductMaster).delete()
        session.commit()
        print("✅ 全ての商品データを削除しました。")
    except Exception as e:
        print(f"❌ 削除中にエラーが発生しました: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    delete_all()
    