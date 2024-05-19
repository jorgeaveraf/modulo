import graphene
import graphql_jwt
import easyenroll.schema
import users.schema
import groups.schema


class Query(users.schema.Query,
            easyenroll.schema.Query,
            groups.schema.Query,
            graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation,
               easyenroll.schema.Mutation,
                groups.schema.Mutation,
               graphene.ObjectType
               ):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
