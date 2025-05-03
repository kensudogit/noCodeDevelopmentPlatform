# FastAPIのAPIRouterをインポート
from fastapi import APIRouter, Depends
# データベースと認証関連のモジュールをインポート
from backend.db import apps, database
from backend.auth import get_current_tenant

# APIRouterのインスタンスを作成
router = APIRouter()

@router.post("/api/apps")
# 新しいアプリを作成するエンドポイント
async def create_app(app: dict, tenant_id: str = Depends(get_current_tenant)):
    # データベースに新しいアプリを挿入するクエリを作成
    query = apps.insert().values(
        tenant_id=tenant_id,
        name=app["name"],
        description=app["description"],
        layout_json=app["layout"],
        workflows_json=app["workflows"]
    )
    # クエリを実行してデータベースに挿入
    await database.execute(query)
    # 成功ステータスを返す
    return {"status": "success"}
