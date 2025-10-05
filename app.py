import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db_control import crud, mymodels

app = FastAPI()

# CORSミドルウェアの設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydanticモデル（APIの入出力の型定義）
class CustomerIn(BaseModel):
    customer_id: str
    customer_name: str
    age: int
    gender: str

class CustomerOut(BaseModel):
    customer_id: str
    customer_name: str
    age: int
    gender: str

    class Config:
        orm_mode = True

# ========== APIエンドポイントの定義 ==========

@app.get("/allcustomers")
def read_all_customers():
    """全顧客情報を取得する"""
    result_json = crud.myselectAll(mymodels.Customer)
    if result_json is None:
        raise HTTPException(status_code=404, detail="Customers not found")
    return json.loads(result_json)

@app.get("/customers")
def read_customer(customer_id: str):
    """指定されたIDの顧客情報を取得する"""
    result_json = crud.myselect(mymodels.Customer, customer_id)
    if result_json is None or result_json == "[]":
        raise HTTPException(status_code=404, detail="Customer not found")
    return json.loads(result_json)[0]

@app.post("/customers")
def create_customer(customer: CustomerIn):
    """新しい顧客情報を作成する"""
    values = customer.dict()

    # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    # ここからがID重複チェックの追加部分です
    # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    # データベースに同じIDの顧客がすでに存在するかチェック
    existing_customer = crud.myselect(mymodels.Customer, values["customer_id"])
    
    # もしデータが存在すれば (空のリストではない場合)
    if existing_customer and existing_customer != "[]":
        # HTTP 409 Conflict エラーを発生させる
        raise HTTPException(
            status_code=409, 
            detail="この顧客IDはすでに登録されています。"
        )
    # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    # ここまでが追加部分です
    # ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

    # IDが存在しない場合のみ、挿入処理に進む
    result = crud.myinsert(mymodels.Customer, values)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to create customer")
    
    created_customer_json = crud.myselect(mymodels.Customer, values["customer_id"])
    return json.loads(created_customer_json)[0]

@app.put("/customers")
def update_customer(customer: CustomerIn):
    """顧客情報を更新する"""
    values = customer.dict()
    result_json = crud.myupdate(mymodels.Customer, values)
    if result_json is None:
        raise HTTPException(status_code=404, detail="Update failed or customer not found")
    return json.loads(result_json)[0]

@app.delete("/customers")
def delete_customer(customer_id: str):
    """顧客情報を削除する"""
    result = crud.mydelete(mymodels.Customer, customer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Delete failed or customer not found")
    return {"message": result}
