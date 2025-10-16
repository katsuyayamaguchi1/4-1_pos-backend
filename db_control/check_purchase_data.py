# db_control/check_purchase_data.py
from sqlalchemy.orm import sessionmaker
from mymodels_MySQL import Transaction, TransactionDetail
from connect_MySQL import engine

def check_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        print("\n--- 取引テーブル (transactions) ---")
        transactions = session.query(Transaction).all()
        if not transactions:
            print("データがありません。")
        else:
            for t in transactions:
                print(f"  取引ID: {t.TRD_ID}, 合計金額: {t.TOTAL_AMT}, 取引日時: {t.DATETIME}")

        print("\n--- 取引明細テーブル (transaction_details) ---")
        details = session.query(TransactionDetail).all()
        if not details:
            print("データがありません。")
        else:
            for d in details:
                print(f"  取引ID: {d.TRD_ID}, 商品名: {d.PRD_NAME}, 単価: {d.PRD_PRICE}")
    finally:
        session.close()

if __name__ == "__main__":
    check_data()
    