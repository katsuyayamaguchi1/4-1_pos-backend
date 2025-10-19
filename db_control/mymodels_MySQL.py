# db_control/mymodels_MySQL.py

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, TIMESTAMP, text
from datetime import datetime

class Base(DeclarativeBase):
    pass

# 商品マスタ
class ProductMaster(Base):
    __tablename__ = 'product_master'
    PRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CODE: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    NAME: Mapped[str] = mapped_column(String(50), nullable=False)
    PRICE: Mapped[int] = mapped_column(Integer, nullable=False)

# 取引テーブル
class Transaction(Base):
    __tablename__ = 'transactions'
    TRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    DATETIME: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    EMP_CD: Mapped[str] = mapped_column(String(10))
    STORE_CD: Mapped[str] = mapped_column(String(5))
    POS_NO: Mapped[str] = mapped_column(String(3))
    TOTAL_AMT: Mapped[int] = mapped_column(Integer)
    TTL_AMT_EX_TAX: Mapped[int] = mapped_column(Integer)

# 取引明細テーブル
class TransactionDetail(Base):
    __tablename__ = 'transaction_details'
    TRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    DTL_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    PRD_ID: Mapped[int] = mapped_column(Integer)
    PRD_CODE: Mapped[str] = mapped_column(String(13))
    PRD_NAME: Mapped[str] = mapped_column(String(50))
    PRD_PRICE: Mapped[int] = mapped_column(Integer)
    TAX_CD: Mapped[str] = mapped_column(String(2))


#以下、STEP4-1level1ベース

# mymodels_MySQL.py

# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import String, Integer, TIMESTAMP, text
# from datetime import datetime

# class Base(DeclarativeBase):
#     pass

# # 1. 商品マスタ
# class ProductMaster(Base):
#     __tablename__ = 'product_master' # テーブル名
#     PRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     CODE: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
#     NAME: Mapped[str] = mapped_column(String(50), nullable=False)
#     PRICE: Mapped[int] = mapped_column(Integer, nullable=False)

# # 2. 取引テーブル
# class Transaction(Base):
#     __tablename__ = 'transactions' # テーブル名
#     TRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     DATETIME: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
#     EMP_CD: Mapped[str] = mapped_column(String(10))
#     STORE_CD: Mapped[str] = mapped_column(String(5))
#     POS_NO: Mapped[str] = mapped_column(String(3))
#     TOTAL_AMT: Mapped[int] = mapped_column(Integer)

# 3. 取引明細テーブル
# class TransactionDetail(Base):
#     __tablename__ = 'transaction_details' # テーブル名
#     TRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
#     DTL_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     PRD_ID: Mapped[int] = mapped_column(Integer)
#     PRD_CODE: Mapped[str] = mapped_column(String(13))
#     PRD_NAME: Mapped[str] = mapped_column(String(50))
#     PRD_PRICE: Mapped[int] = mapped_column(Integer)


# 以下、STEP3ベース

# from sqlalchemy import String
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# class Base(DeclarativeBase):
#     pass

# class Customer(Base):
#     __tablename__ = 'customers'
    
#     # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
#     # MySQLのルールに従い、String(255) のように最大文字数を指定します
#     # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
#     customer_id: Mapped[str] = mapped_column(String(255), primary_key=True)
#     customer_name: Mapped[str] = mapped_column(String(255))
#     age: Mapped[int] = mapped_column()
#     gender: Mapped[str] = mapped_column(String(255))