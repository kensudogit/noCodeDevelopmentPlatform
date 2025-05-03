# ストロベリーをインポート
import strawberry
# 非同期ジェネレーターの型をインポート
from typing import AsyncGenerator
# FastAPIをインポート
from fastapi import FastAPI
# ストロベリーのGraphQLルーターをインポート
from strawberry.fastapi import GraphQLRouter
# 非同期処理のためのモジュールをインポート
import asyncio

# アイテムを表すクラス
@strawberry.type
class Item:
    id: int  # アイテムのID
    data: str  # アイテムのデータ

# メモリにストアする（本来はDB）
items = []

# 追加されたときに通知するための購読者のセット
subscribers = set()

# サブスクリプションを表すクラス
@strawberry.type
class Subscription:
    # アイテムが追加されたときに通知する非同期ジェネレーター
    @strawberry.subscription
    async def on_item_added(self) -> AsyncGenerator[Item, None]:
        queue = asyncio.Queue()  # 非同期キューを作成
        subscribers.add(queue)  # 購読者にキューを追加
        try:
            while True:
                item = await queue.get()  # キューからアイテムを取得
                yield item  # アイテムを返す
        finally:
            subscribers.remove(queue)  # 購読者からキューを削除

# ミューテーションを表すクラス
@strawberry.type
class Mutation:
    # アイテムを追加する非同期ミューテーション
    @strawberry.mutation
    async def add_item(self, data: str) -> Item:
        new_item = Item(id=len(items) + 1, data=data)  # 新しいアイテムを作成
        items.append(new_item)  # アイテムをリストに追加
        for subscriber in subscribers:
            await subscriber.put(new_item)  # 購読者に新しいアイテムを通知
        return new_item  # 新しいアイテムを返す

# クエリを表すクラス
@strawberry.type
class Query:
    # すべてのアイテムを取得するフィールド
    @strawberry.field
    def all_items(self) -> list[Item]:
        return items  # アイテムのリストを返す

# スキーマを作成
schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

# FastAPIアプリケーションを作成
app = FastAPI()
# GraphQLルーターを作成
graphql_app = GraphQLRouter(schema)

# ルーターをアプリケーションに追加
app.include_router(graphql_app, prefix="/graphql")
