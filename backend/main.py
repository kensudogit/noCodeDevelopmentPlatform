# backend/main.py
from fastapi import FastAPI
from ariadne.asgi import GraphQL
import graphene
import databases
import sqlalchemy
import os
from backend.auth import auth_backend
from fastapi_users import FastAPIUsers
from backend.dynamic_schema import build_dynamic_schema
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

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

# Create the GraphQL schema using graphene
schema = graphene.Schema(query=Query, mutation=Mutation)

# Add the GraphQL route using Ariadne
app.add_route("/graphql", GraphQL(schema, debug=True))

# DB接続設定
DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
)

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# テーブル定義
# 動的フィールドを格納するテーブル
# 各フィールドはID、名前、タイプを持つ
dynamic_fields = sqlalchemy.Table(
    "dynamic_fields",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String),
)

# 動的アイテムを格納するテーブル
# 各アイテムはIDとJSON形式のデータを持つ
dynamic_items = sqlalchemy.Table(
    "dynamic_items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("data", sqlalchemy.JSON),
)

engine = sqlalchemy.create_engine(DATABASE_URL.replace("+asyncpg", ""))
metadata.create_all(engine)

# 仮ユーザークラス（本来はDB管理する）
# ユーザー情報を管理するためのクラス
class UserDB:
    id = "user_id"
    email = "test@example.com"
    is_active = True
    is_superuser = False

# ユーザーを取得する非同期関数
async def get_user(user_id):
    return UserDB()

# FastAPIユーザーのインスタンスを作成
# 認証バックエンドを使用してユーザー管理を行う
fastapi_users = FastAPIUsers(
    get_user_manager=get_user,
    auth_backends=[auth_backend],
)

# JWTログインAPI追加
# JWTを使用した認証ルーターを追加
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# GraphQLモデル
# 動的フィールドのGraphQLオブジェクトタイプ
class DynamicFieldType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    type = graphene.String()

# 動的アイテムのGraphQLオブジェクトタイプ
class DynamicItemType(graphene.ObjectType):
    id = graphene.Int()
    data = graphene.JSONString()

# Query
# データベースからフィールドとアイテムを取得するためのクエリ
class Query(graphene.ObjectType):
    fields = graphene.List(DynamicFieldType)
    items = graphene.List(DynamicItemType)

    # フィールドを解決する非同期関数
    async def resolve_fields(self, info):
        query = dynamic_fields.select()
        return await database.fetch_all(query)

    # アイテムを解決する非同期関数
    async def resolve_items(self, info):
        query = dynamic_items.select()
        return await database.fetch_all(query)

# Mutation
# 新しいフィールドを作成するためのミューテーション
class CreateField(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        type = graphene.String(required=True)

    field = graphene.Field(lambda: DynamicFieldType)

    # フィールドを作成する非同期関数
    async def mutate(self, info, name, type):
        query = dynamic_fields.insert().values(name=name, type=type)
        field_id = await database.execute(query)
        return CreateField(field={"id": field_id, "name": name, "type": type})

# 新しいアイテムを作成するためのミューテーション
class CreateItem(graphene.Mutation):
    class Arguments:
        data = graphene.JSONString(required=True)

    item = graphene.Field(lambda: DynamicItemType)

    # アイテムを作成する非同期関数
    async def mutate(self, info, data):
        # バリデーション追加
        # 登録されているフィールド名を取得
        fields_query = dynamic_fields.select()
        registered_fields = await database.fetch_all(fields_query)

        # データのフィールド名が登録済みのフィールド名に含まれているか確認
        valid_field_names = {f["name"] for f in registered_fields}
        if not set(data.keys()).issubset(valid_field_names):
            raise ValueError("Invalid fields detected.")

        # アイテムをデータベースに挿入
        query = dynamic_items.insert().values(data=data)
        item_id = await database.execute(query)
        return CreateItem(item={"id": item_id, "data": data})

# Mutation
# フィールドとアイテムを作成するためのミューテーションを定義
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
