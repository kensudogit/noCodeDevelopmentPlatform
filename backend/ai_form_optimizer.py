# OpenAIのAPIをインポート
import openai
# FastAPIのAPIRouterをインポート
from fastapi import APIRouter

# APIRouterのインスタンスを作成
router = APIRouter()

# OpenAIのAPIキーを設定
openai.api_key = "your_openai_api_key"

# POSTリクエストを受け取るエンドポイントを定義
@router.post("/api/ai/optimize-form")
async def optimize_form(layout: dict):
    # フォーム設計を改善するためのプロンプトを作成
    prompt = f"""
    次のフォーム設計をより使いやすく改善提案してください。
    フォーム定義: {layout}
    改善ポイントをJSONで返してください（例：フィールド名の変更、必須設定の追加、並び順変更など）
    """
    # OpenAIのChatCompletionを使用して応答を生成
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたはUX設計のエキスパートです。"},
            {"role": "user", "content": prompt}
        ]
    )

    # 応答の最初の選択肢を返す
    return {"suggestion": response.choices[0].message["content"]}
