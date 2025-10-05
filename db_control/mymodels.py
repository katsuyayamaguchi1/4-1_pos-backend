from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# クラス名は 'Customer' (単数形)
class Customer(Base):
    __tablename__ = 'customers'
    
    # カラム名はフロントエンドやPDFの演習内容と一致させる
    customer_id: Mapped[str] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column()