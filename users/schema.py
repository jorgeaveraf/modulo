from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import Group


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class UserType(DjangoObjectType):
    groups = graphene.List(GroupType)
    
    class Meta:
        model = get_user_model()

    def resolve_groups(self, info):
        return self.groups.all()
    
    def resolver_first_name(self, info):
        return self.first_name


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)  # Agrega el campo 'me' para representar al usuario actual

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Debes estar autenticado para acceder a esta información.')
        return user  # Devuelve el usuario actualmente autenticado

    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        is_superuser = graphene.Boolean()

    def mutate(self, info, username, password, email, is_superuser=False):
        user = get_user_model()(
            username=username,
            email=email,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
