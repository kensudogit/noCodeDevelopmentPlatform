from fastapi import APIRouter, Depends
from backend.db import workflows, database
from backend.auth import get_current_tenant

router = APIRouter()

@router.post("/api/workflows")
async def save_workflow(workflow: dict, tenant_id: str = Depends(get_current_tenant)):
    query = workflows.insert().values(
        tenant_id=tenant_id,
        workflow_json=workflow
    )
    await database.execute(query)
    return {"status": "success"}
async def trigger_workflows(item_data, tenant_id):
    flows = await database.fetch_all(workflows.select().where(workflows.c.tenant_id == tenant_id))
    for flow in flows:
        if eval_condition(item_data, flow["workflow_json"]["if"]):
            await execute_action(flow["workflow_json"]["then"])
        else:
            await execute_action(flow["workflow_json"]["else"])

def eval_condition(item_data, condition):
    value = item_data.get(condition["field"])
    if condition["operator"] == "==":
        return value == condition["value"]
    if condition["operator"] == ">":
        return value > int(condition["value"])
    if condition["operator"] == "<":
        return value < int(condition["value"])
    return False

async def execute_action(action):
    if action["action"] == "send_email":
        print("メール送信する！（ここは本番なら実際に送信API呼び出し）")
    if action["action"] == "notify_admin":
        print("管理者に通知する！")
