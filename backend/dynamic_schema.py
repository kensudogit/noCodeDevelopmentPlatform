# backend/dynamic_schema.py
import graphene
from backend.db import database, dynamic_fields, dynamic_items  # DB定義を使う

def map_field_type(type_name):
    mapping = {
        "String": graphene.String,
        "Int": graphene.Int,
        "Boolean": graphene.Boolean,
    }
    return mapping.get(type_name, graphene.String)

async def build_dynamic_schema():
    # DBからフィールドリストを取得
    fields_data = await database.fetch_all(dynamic_fields.select())

    # 動的オブジェクトを作る
    dynamic_fields_dict = {}
    for field in fields_data:
        dynamic_fields_dict[field["name"]] = graphene.Field(map_field_type(field["type"]))

    # GraphQLタイプを定義
    DynamicItemType = type(
        "DynamicItemType",
        (graphene.ObjectType,),
        dynamic_fields_dict,
    )

    # Query
    class Query(graphene.ObjectType):
        items = graphene.List(DynamicItemType)

        async def resolve_items(self, info):
            records = await database.fetch_all(dynamic_items.select())
            result = []
            for rec in records:
                result.append(rec["data"])  # JSONBなのでそのまま返す
            return result

    # Mutation（登録）
    class CreateItem(graphene.Mutation):
        class Arguments:
            data = graphene.JSONString(required=True)

        item = graphene.Field(DynamicItemType)

        async def mutate(self, info, data):
            # 簡単なバリデーション
            allowed_fields = {field["name"] for field in fields_data}
            if not set(data.keys()).issubset(allowed_fields):
                raise Exception("Invalid fields detected.")

            query = dynamic_items.insert().values(data=data)
            item_id = await database.execute(query)
            return CreateItem(item=data)

    class Mutation(graphene.ObjectType):
        create_item = CreateItem.Field()

    # スキーマ生成
    return graphene.Schema(query=Query, mutation=Mutation)
