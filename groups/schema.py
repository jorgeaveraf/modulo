# groups/schema.py
from django.contrib.auth.models import Group
import graphene
from graphene_django import DjangoObjectType

class GroupType(DjangoObjectType):
    class Meta:
        model = Group

class CreateGroup(graphene.Mutation):
    group = graphene.Field(GroupType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        group = Group(name=name)
        group.save()
        return CreateGroup(group=group)

class Query(graphene.ObjectType):
    groups = graphene.List(GroupType)

    def resolve_groups(self, info):
        return Group.objects.all()

class Mutation(graphene.ObjectType):
    create_group = CreateGroup.Field()
