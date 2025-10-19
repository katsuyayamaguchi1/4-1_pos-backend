# db_control/check_data.py

from sqlalchemy.orm import sessionmaker
from mymodels_MySQL import ProductMaster, Transaction, TransactionDetail
from connect_MySQL import engine

def check_all_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("\n--- 🟢 商品マスタ (product_master) ---")
        products = session.query(ProductMaster).all()
        if not products:
            print("データがありません。")
        else:
            for p in products:
                print(f"  CODE: {p.CODE}, NAME: {p.NAME}, PRICE: {p.PRICE}")

        print("\n--- 🔵 取引テーブル (transactions) ---")
        transactions = session.query(Transaction).all()
        if not transactions:
            print("データがありません。")
        else:
            # カラムの存在チェックを兼ねて表示
            for t in transactions:
                print(f"  取引ID: {t.TRD_ID}, 税抜合計: {t.TTL_AMT_EX_TAX}")

        print("\n--- 🟡 取引明細テーブル (transaction_details) ---")
        details = session.query(TransactionDetail).all()
        if not details:
            print("データがありません。")
        else:
            # カラムの存在チェックを兼ねて表示
            for d in details:
                print(f"  取引ID: {d.TRD_ID}, 税区分: {d.TAX_CD}")

    except Exception as e:
        print(f"\n❌ データの確認中にエラーが発生しました: {e}")
        print("テーブル構造が古い可能性があります。drop_all_tables.py と create_tables_MySQL.py を実行しましたか？")
    finally:
        session.close()

if __name__ == "__main__":
    check_all_data()