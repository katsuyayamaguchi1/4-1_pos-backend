import os
from dotenv import load_dotenv
load_dotenv()

ENGINE = os.getenv("DB_ENGINE", "sqlite")

if ENGINE == "mysql":
    from .connect_MySQL import engine, SessionLocal
    from .mymodels_MySQL import Base, Customer
else:
    from .connect import engine, SessionLocal
    from .mymodels import Base, Customer
