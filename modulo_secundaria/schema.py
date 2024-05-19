import graphene
import easyenroll.schema
import users.schema


class Query(users.schema.Query, easyenroll.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, easyenroll.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
