import openai
from fastapi import APIRouter

# FastAPIのルーターを作成
router = APIRouter()

# OpenAIのAPIキーを設定（本番環境では環境変数を使用することを推奨）
openai.api_key = "your_openai_api_key"  # 本番では環境変数にしてください！

# AIフィールド提案のエンドポイントを定義
@router.post("/ai/field-suggestions")
async def suggest_fields(prompt: str):
    # OpenAIのChatCompletionを使用してフィールドを提案
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたはデータベース設計のアシスタントです。次の要求に応じてフィールド一覧を提案してください。フィールド名と型をJSON形式で返してください。型はString/Int/Boolean/Dateのいずれかにしてください。"},
            {"role": "user", "content": prompt}
        ]
    )

    # レスポンスからコンテンツを取得
    content = response.choices[0].message["content"]

    # JSON形式で返すことを想定
    return {"fields": content}
