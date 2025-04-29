from fastapi import APIRouter, Depends
from backend.db import layouts, database
from backend.auth import get_current_tenant

router = APIRouter()

@router.post("/api/layouts")
async def save_layout(layout: dict, tenant_id: str = Depends(get_current_tenant)):
    query = layouts.insert().values(
        tenant_id=tenant_id,
        layout_json=layout
    )
    await database.execute(query)
    return {"status": "success"}
