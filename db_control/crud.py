# db_control/crud.py

from sqlalchemy.orm import sessionmaker
from typing import List

from .mymodels_MySQL import ProductMaster, Transaction, TransactionDetail
from .connect_MySQL import engine

def get_product(product_code: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        result = session.query(ProductMaster).filter(ProductMaster.CODE == product_code).first()
        
        if not result:
            return None
        
        # ★★★★★★★【ここを修正】★★★★★★★
        # 全てのキー名をPydanticモデルと一致させます
        product_dict = {
            "PRD_ID": result.PRD_ID,
            "PRD_CODE": result.CODE,
            "PRD_NAME": result.NAME,
            "PRD_PRICE": result.PRICE
        }
        # ★★★★★★★【ここまで修正】★★★★★★★
        return product_dict

    except Exception as e:
        print(f"商品検索中にエラーが発生しました: {e}")
        return None
    finally:
        session.close()

def create_purchase(products: List[dict]):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        new_transaction = Transaction(
            EMP_CD='9999999999',
            STORE_CD='30',
            POS_NO='90',
            TOTAL_AMT=0
        )
        session.add(new_transaction)
        session.flush()

        total_amount = 0
        for p in products:
            new_detail = TransactionDetail(
                TRD_ID=new_transaction.TRD_ID,
                PRD_ID=p.PRD_ID,
                PRD_CODE=p.PRD_CODE,
                PRD_NAME=p.PRD_NAME,
                PRD_PRICE=p.PRD_PRICE
            )
            session.add(new_detail)
            total_amount += p.PRD_PRICE
        
        new_transaction.TOTAL_AMT = total_amount
        session.commit()
        return {"total_amount": total_amount}

    except Exception as e:
        print(f"購入処理中にエラーが発生しました: {e}")
        session.rollback()
        return None
    finally:
        session.close()



# 以下、STEP3ベース

# # uname() error回避
# import platform
# print("platform", platform.uname())

# from sqlalchemy import create_engine, insert, delete, update, select
# import sqlalchemy
# from sqlalchemy.orm import sessionmaker
# import json
# import pandas as pd

# # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# # ここからが接続先の切り替え部分です
# # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# # SQLite用のimport文をコメントアウト（行頭に#を付ける）
# # from db_control.connect import engine
# # from db_control.mymodels import Customer

# # MySQL用のimport文を有効にする
# from db_control.connect_MySQL import engine
# from db_control.mymodels_MySQL import Customer
# # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# # ここまでが修正部分です
# # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

# def myinsert(mymodel, values):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = insert(mymodel).values(values)
#     try:
#         with session.begin():
#             session.execute(query)
#         return "inserted"
#     except sqlalchemy.exc.IntegrityError as e:
#         print(f"一意制約違反により、挿入に失敗しました: {e}")
#         session.rollback()
#         return None
#     finally:
#         session.close()

# def myselect(mymodel, customer_id: str):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
#     try:
#         with session.begin():
#             result = query.all()
#         result_dict_list = [
#             {
#                 "customer_id": c.customer_id,
#                 "customer_name": c.customer_name,
#                 "age": c.age,
#                 "gender": c.gender
#             }
#             for c in result
#         ]
#         return json.dumps(result_dict_list, ensure_ascii=False)
#     except Exception as e:
#         print(f"Select failed: {e}")
#         return None
#     finally:
#         session.close()

# def myselectAll(mymodel):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = select(mymodel)
#     try:
#         with session.begin():
#             df = pd.read_sql_query(query, con=engine)
#             result_json = df.to_json(orient='records', force_ascii=False)
#         return result_json
#     except Exception as e:
#         print(f"Select all failed: {e}")
#         return None
#     finally:
#         session.close()

# def myupdate(mymodel, values: dict):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     customer_id = values.get("customer_id")
#     if not customer_id:
#         session.close()
#         return None
#     try:
#         query = (
#             update(mymodel)
#             .where(mymodel.customer_id == customer_id)
#             .values(**values)
#         )
#         with session.begin():
#             session.execute(query)
#         return myselect(mymodel, customer_id)
#     except Exception as e:
#         print(f"更新に失敗しました: {e}")
#         session.rollback()
#         return None
#     finally:
#         session.close()

# def mydelete(mymodel, customer_id: str):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = delete(mymodel).where(mymodel.customer_id == customer_id)
#     try:
#         with session.begin():
#             session.execute(query)
#         return f"{customer_id} is deleted"
#     except Exception as e:
#         print(f"削除に失敗しました: {e}")
#         session.rollback()
#         return None
#     finally:
#         session.close()