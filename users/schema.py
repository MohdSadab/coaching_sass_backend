import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token, get_token

from graphene import relay

import graphene
import graphql_jwt
from .models import User
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token, get_token
from .services import UserService
class UserType(DjangoObjectType):
    class Meta:
        model = User
        

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=False)
        role = graphene.String(required=True)

    def mutate(self, info, username, password, email,first_name, last_name, role):
        
        if UserService.is_email_exists(email):
            raise Exception('Email already exists')
        if UserService.is_username_exists(username):
            raise Exception('Username already exists')
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        user.save()
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        return CreateUser(user=user, token=token, refresh_token=refresh_token)


class UpdateUser(graphene.Mutation):

    
    user = graphene.Field(UserType)
    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=False)
        role = graphene.String(required=True)
        status = graphene.String(required=True)
        is_deleted = graphene.Boolean(required=True)
        plan = graphene.String(required=True)
        verified = graphene.Boolean(required=True)
        profile_img = graphene.String(required=False)
        street = graphene.String(required=False)
        city = graphene.String(required=False)
        state = graphene.String(required=False)
        pin_code = graphene.String(required=False)
        description = graphene.String(required=False)
        phone_no = graphene.String(required=False)
        birth_date = graphene.Date(required=False)
        standard = graphene.String(required=False)

    @login_required
    def mutate(self, info, id, first_name, last_name, role, status, is_deleted, plan, verified, profile_img, street, city, state, pin_code, description, phone_no, birth_date, standard):
        user = UserService.get_user_by_id(id)
        user.first_name = first_name
        user.last_name = last_name
        user.role = role
        user.status = status
        user.is_deleted = is_deleted
        user.plan = plan
        user.verified = verified
        user.profile_img = profile_img
        user.street = street
        user.city = city
        user.state = state
        user.pin_code = pin_code
        user.description = description
        user.phone_no = phone_no
        user.birth_date = birth_date
        user.standard = standard
        user.save()
        return UpdateUser(user=user)
    


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)
    
    def resolve_whoami(self, info):
        user = info.context.user
        # Check if user is authenticated
        if user.is_anonymous:
            raise Exception("Authentication Failure: Your must be signed in")
        return user
  

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()

   
schema = graphene.Schema(query=Query, mutation=Mutation)