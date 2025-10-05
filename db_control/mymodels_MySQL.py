from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = 'customers'
    
    # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    # MySQLのルールに従い、String(255) のように最大文字数を指定します
    # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    customer_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column(String(255))