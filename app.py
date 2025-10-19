# backend/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000", # ローカル開発用
    "https://app-002-gen10-step3-1-node-oshima6.azurewebsites.net", # 本番環境のフロントエンドURL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from db_control import crud

# スモークテストをパスさせるためのトップページ
@app.get("/")
def read_root():
    return {"message": "POS Backend is running"}

# --- データモデル定義 ---
class Product(BaseModel):
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int

class PurchaseRequest(BaseModel):
    products: List[Product]

# --- POSアプリ用API ---
@app.get("/products/{product_code}")
def get_product_by_code(product_code: str):
    print(f"受け取った商品コード: {product_code}")
    product = crud.get_product(product_code)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/purchase")
def create_purchase(req: PurchaseRequest):
    # ★★★★★【この行を追加】★★★★★
    print("--- /purchase endpoint called ---")
    # ★★★★★★★★★★★★★★★★★★

    print(f"受け取った購入リスト: {req}") # 念のためこちらも残す
    result = crud.create_purchase(req.products)
    if not result:
        raise HTTPException(status_code=500, detail="Purchase failed")
    return result