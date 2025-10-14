import json
import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from db_control import crud, mymodels

app = FastAPI(title="POS Backend API")

# =========================
# CORS 設定
# =========================
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://app-002-gen10-step3-1-node-oshima6.azurewebsites.net",  # フロント本番
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,          # 認証付きCookieを使わないなら False でもOK
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Pydantic モデル
# =========================
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

# =========================
# ヘルスチェック
# =========================
@app.get("/")
def health():
    return {"status": "ok"}

# =========================
# API エンドポイント
# =========================
@app.get("/allcustomers")
def read_all_customers():
    """全顧客情報を取得"""
    result_json = crud.myselectAll(mymodels.Customer)
    if result_json is None:
        raise HTTPException(status_code=404, detail="Customers not found")
    return json.loads(result_json)

@app.get("/customers")
def read_customer(customer_id: str):
    """指定IDの顧客情報を取得"""
    result_json = crud.myselect(mymodels.Customer, customer_id)
    if result_json is None or result_json == "[]":
        raise HTTPException(status_code=404, detail="Customer not found")
    return json.loads(result_json)[0]

@app.post("/customers")
def create_customer(customer: CustomerIn):
    """顧客を新規作成（ID重複チェックあり）"""
    values = customer.dict()

    # 既存チェック
    existing = crud.myselect(mymodels.Customer, values["customer_id"])
    if existing and existing != "[]":
        raise HTTPException(status_code=409, detail="この顧客IDはすでに登録されています。")

    result = crud.myinsert(mymodels.Customer, values)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to create customer")

    created = crud.myselect(mymodels.Customer, values["customer_id"])
    return json.loads(created)[0]

@app.put("/customers")
def update_customer(customer: CustomerIn):
    """顧客情報を更新"""
    values = customer.dict()
    result_json = crud.myupdate(mymodels.Customer, values)
    if result_json is None:
        raise HTTPException(status_code=404, detail="Update failed or customer not found")
    return json.loads(result_json)[0]

@app.delete("/customers")
def delete_customer(customer_id: str):
    """顧客情報を削除"""
    result = crud.mydelete(mymodels.Customer, customer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Delete failed or customer not found")
    return {"message": result}

# =========================
# 例外ハンドラ（500の詳細確認用）
# =========================
@app.exception_handler(Exception)
async def dump_traceback(request: Request, exc: Exception):
    return PlainTextResponse("TRACEBACK:\n" + traceback.format_exc(), status_code=500)

