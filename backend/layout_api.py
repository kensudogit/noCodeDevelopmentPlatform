# FastAPIのAPIRouterをインポート
from fastapi import APIRouter, Depends
# データベースと認証関連のモジュールをインポート
from backend.db import layouts, database
from backend.auth import get_current_tenant

# APIRouterのインスタンスを作成
router = APIRouter()

# 新しいレイアウトを保存するエンドポイント
@router.post("/api/layouts")
async def save_layout(layout: dict, tenant_id: str = Depends(get_current_tenant)):
    # レイアウトをデータベースに挿入するクエリを作成
    query = layouts.insert().values(
        tenant_id=tenant_id,
        layout_json=layout
    )
    # クエリを実行してデータベースに保存
    await database.execute(query)
    # 成功ステータスを返す
    return {"status": "success"}
