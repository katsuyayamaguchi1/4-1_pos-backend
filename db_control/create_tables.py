# 相対インポートではなく、プロジェクトルートからの絶対インポートに修正
from db_control.mymodels import Base
from db_control.connect import engine

def create_database():
    """
    mymodels.pyで定義されたモデルに基づいてデータベースとテーブルを作成します。
    """
    try:
        print("データベースとテーブルを作成します...")
        # mymodels.pyで定義されたすべてのテーブルを作成
        Base.metadata.create_all(bind=engine)
        print("作成が完了しました。")
    except Exception as e:
        print(f"作成中にエラーが発生しました: {e}")

if __name__ == "__main__":
    create_database()
