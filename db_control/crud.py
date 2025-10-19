# db_control/crud.py

from sqlalchemy.orm import sessionmaker
from typing import List
import math

from .mymodels_MySQL import ProductMaster, Transaction, TransactionDetail
from .connect_MySQL import engine

def get_product(product_code: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        result = session.query(ProductMaster).filter(ProductMaster.CODE == int(product_code)).first()
        if not result:
            return None
        product_dict = {
            "PRD_ID": result.PRD_ID,
            "PRD_CODE": str(result.CODE),
            "PRD_NAME": result.NAME,
            "PRD_PRICE": result.PRICE
        }
        print(f"デバッグ情報 -> PRD_CODEの型: {type(product_dict['PRD_CODE'])}")
        return product_dict
    except Exception as e:
        print(f"商品検索中にエラーが発生しました: {e}")
        return None
    finally:
        session.close()

# ★★★★★★★【ここからが最終修正箇所】★★★★★★★
def create_purchase(products: List): # 型ヒントを Pydanticモデルのリストに変更してもOK
    """
    購入リストを基に、税計算を行いながら取引・取引明細テーブルにデータを登録する
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        new_transaction = Transaction(
            EMP_CD='9999999999',
            STORE_CD='30',
            POS_NO='90',
            TOTAL_AMT=0,
            TTL_AMT_EX_TAX=0
        )
        session.add(new_transaction)
        session.flush()

        total_amount_incl_tax = 0
        for p in products:
            # 【重要】リストの中身はPydanticモデルのオブジェクトなので、ドット記法でアクセス
            total_amount_incl_tax += p.PRD_PRICE # p['PRD_PRICE'] ではなく p.PRD_PRICE

        total_amount_ex_tax = math.floor(total_amount_incl_tax / 1.1)

        for p in products:
             # 【重要】同様にドット記法でアクセス
            new_detail = TransactionDetail(
                TRD_ID=new_transaction.TRD_ID,
                PRD_ID=p.PRD_ID,       # p['PRD_ID'] ではなく p.PRD_ID
                PRD_CODE=p.PRD_CODE,   # p['PRD_CODE'] ではなく p.PRD_CODE
                PRD_NAME=p.PRD_NAME,   # p['PRD_NAME'] ではなく p.PRD_NAME
                PRD_PRICE=p.PRD_PRICE, # p['PRD_PRICE'] ではなく p.PRD_PRICE
                TAX_CD='10'
            )
            session.add(new_detail)

        new_transaction.TOTAL_AMT = total_amount_incl_tax
        new_transaction.TTL_AMT_EX_TAX = total_amount_ex_tax

        session.commit()

        return {
            "total_amount": total_amount_incl_tax,
            "total_amount_ex_tax": total_amount_ex_tax
        }

    except Exception as e:
        # エラー発生時のログ出力を強化
        print(f"購入処理中に予期せぬエラーが発生しました: {e}")
        import traceback
        traceback.print_exc() # 詳細なトレースバックを出力
        session.rollback()
        return None
    finally:
        session.close()
# ★★★★★★★【ここまでが最終修正箇所】★★★★★★★