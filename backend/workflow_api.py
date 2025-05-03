# FastAPIのAPIRouterをインポート
from fastapi import APIRouter, Depends
# データベースと認証関連のモジュールをインポート
from backend.db import workflows, database
from backend.auth import get_current_tenant

# ルーターのインスタンスを作成
router = APIRouter()

# 新しいワークフローを保存するエンドポイント
@router.post("/api/workflows")
async def save_workflow(workflow: dict, tenant_id: str = Depends(get_current_tenant)):
    # ワークフローをデータベースに挿入するクエリを作成
    query = workflows.insert().values(
        tenant_id=tenant_id,
        workflow_json=workflow
    )
    # クエリを実行
    await database.execute(query)
    return {"status": "success"}

# ワークフローをトリガーする関数
async def trigger_workflows(item_data, tenant_id):
    # 指定されたテナントIDのワークフローをすべて取得
    flows = await database.fetch_all(workflows.select().where(workflows.c.tenant_id == tenant_id))
    for flow in flows:
        # 条件を評価し、アクションを実行
        if eval_condition(item_data, flow["workflow_json"]["if"]):
            await execute_action(flow["workflow_json"]["then"])
        else:
            await execute_action(flow["workflow_json"]["else"])

# 条件を評価する関数
# item_dataから指定されたフィールドの値を取得し、条件と比較
# 条件に基づいてTrueまたはFalseを返す
def eval_condition(item_data, condition):
    value = item_data.get(condition["field"])
    if condition["operator"] == "==":
        return value == condition["value"]
    if condition["operator"] == ">":
        return value > int(condition["value"])
    if condition["operator"] == "<":
        return value < int(condition["value"])
    return False

# アクションを実行する関数
async def execute_action(action):
    # アクションがメール送信の場合
    if action["action"] == "send_email":
        print("メール送信する！（ここは本番なら実際に送信API呼び出し）")
    # アクションが管理者通知の場合
    if action["action"] == "notify_admin":
        print("管理者に通知する！")
