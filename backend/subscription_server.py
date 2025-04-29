import strawberry
from typing import AsyncGenerator
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Item:
    id: int
    data: str

# メモリにストアする（本来はDB）
items = []

# 追加されたときに通知するための購読者のセット
subscribers = set()

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def on_item_added(self) -> AsyncGenerator[Item, None]:
        queue = asyncio.Queue()
        subscribers.add(queue)
        try:
            while True:
                item = await queue.get()
                yield item
        finally:
            subscribers.remove(queue)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_item(self, data: str) -> Item:
        new_item = Item(id=len(items) + 1, data=data)
        items.append(new_item)
        for subscriber in subscribers:
            await subscriber.put(new_item)
        return new_item

@strawberry.type
class Query:
    @strawberry.field
    def all_items(self) -> list[Item]:
        return items

schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
