import openai
from fastapi import APIRouter

router = APIRouter()

openai.api_key = "your_openai_api_key"

@router.post("/api/ai/optimize-form")
async def optimize_form(layout: dict):
    prompt = f"""
    次のフォーム設計をより使いやすく改善提案してください。
    フォーム定義: {layout}
    改善ポイントをJSONで返してください（例：フィールド名の変更、必須設定の追加、並び順変更など）
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたはUX設計のエキスパートです。"},
            {"role": "user", "content": prompt}
        ]
    )

    return {"suggestion": response.choices[0].message["content"]}
