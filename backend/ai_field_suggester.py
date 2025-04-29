import openai
from fastapi import APIRouter

router = APIRouter()

openai.api_key = "your_openai_api_key"  # 本番では環境変数にしてください！

@router.post("/ai/field-suggestions")
async def suggest_fields(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたはデータベース設計のアシスタントです。次の要求に応じてフィールド一覧を提案してください。フィールド名と型をJSON形式で返してください。型はString/Int/Boolean/Dateのいずれかにしてください。"},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message["content"]

    # JSON形式で返すことを想定
    return {"fields": content}
