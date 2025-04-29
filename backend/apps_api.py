from fastapi import APIRouter, Depends
from backend.db import apps, database
from backend.auth import get_current_tenant

router = APIRouter()

@router.post("/api/apps")
async def create_app(app: dict, tenant_id: str = Depends(get_current_tenant)):
    query = apps.insert().values(
        tenant_id=tenant_id,
        name=app["name"],
        description=app["description"],
        layout_json=app["layout"],
        workflows_json=app["workflows"]
    )
    await database.execute(query)
    return {"status": "success"}
