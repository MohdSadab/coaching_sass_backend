# core/schema.py

import graphene

from users import schema as users_schema


class Query(users_schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(users_schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)