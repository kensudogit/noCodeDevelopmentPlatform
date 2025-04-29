# backend/main.py
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
import graphene
import databases
import sqlalchemy
import os
from backend.auth import auth_backend
from fastapi_users import FastAPIUsers
from backend.dynamic_schema import build_dynamic_schema

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# アプリケーション起動時のイベント
@app.on_event("startup")
async def startup():
    await database.connect()
    # 起動時にスキーマビルド
    app.schema = await build_dynamic_schema()

# アプリケーション終了時のイベント
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# GraphQLエンドポイントのミドルウェア
@app.middleware("http")
async def graphql_schema_reload(request, call_next):
    # 毎回スキーマをリロード
    app.schema = await build_dynamic_schema()
    return await call_next(request)

# ルートエンドポイント
@app.get("/")
def root():
    return {"message": "Dynamic GraphQL Server running"}

# GraphQLエンドポイントを追加
app.add_route("/graphql", GraphQLApp(schema=lambda: app.schema))

# DB接続設定
DATABASE_URL = "postgresql+asyncpg://postgres:yourpassword@localhost:5432/yourdbname"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# テーブル定義
dynamic_fields = sqlalchemy.Table(
    "dynamic_fields",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String),
)

dynamic_items = sqlalchemy.Table(
    "dynamic_items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("data", sqlalchemy.JSON),
)

engine = sqlalchemy.create_engine(DATABASE_URL.replace("+asyncpg", ""))
metadata.create_all(engine)

# 仮ユーザークラス（本来はDB管理する）
class UserDB:
    id = "user_id"
    email = "test@example.com"
    is_active = True
    is_superuser = False

async def get_user(user_id):
    return UserDB()

fastapi_users = FastAPIUsers(
    get_user_manager=get_user,
    auth_backends=[auth_backend],
)

# JWTログインAPI追加
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# GraphQLモデル
class DynamicFieldType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    type = graphene.String()

class DynamicItemType(graphene.ObjectType):
    id = graphene.Int()
    data = graphene.JSONString()

# Query
class Query(graphene.ObjectType):
    fields = graphene.List(DynamicFieldType)
    items = graphene.List(DynamicItemType)

    async def resolve_fields(self, info):
        query = dynamic_fields.select()
        return await database.fetch_all(query)

    async def resolve_items(self, info):
        query = dynamic_items.select()
        return await database.fetch_all(query)

# Mutation
class CreateField(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        type = graphene.String(required=True)

    field = graphene.Field(lambda: DynamicFieldType)

    async def mutate(self, info, name, type):
        query = dynamic_fields.insert().values(name=name, type=type)
        field_id = await database.execute(query)
        return CreateField(field={"id": field_id, "name": name, "type": type})

class CreateItem(graphene.Mutation):
    class Arguments:
        data = graphene.JSONString(required=True)

    item = graphene.Field(lambda: DynamicItemType)

    async def mutate(self, info, data):
        # バリデーション追加
        fields_query = dynamic_fields.select()
        registered_fields = await database.fetch_all(fields_query)

        valid_field_names = {f["name"] for f in registered_fields}
        if not set(data.keys()).issubset(valid_field_names):
            raise Exception("Invalid fields detected.")

        query = dynamic_items.insert().values(data=data)
        item_id = await database.execute(query)
        return CreateItem(item={"id": item_id, "data": data})

class Mutation(graphene.ObjectType):
    create_field = CreateField.Field()
    create_item = CreateItem.Field()

# アプリケーション起動時のイベント
@app.on_event("startup")
async def startup():
    await database.connect()

# アプリケーション終了時のイベント
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# GraphQLエンドポイントを追加
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))
