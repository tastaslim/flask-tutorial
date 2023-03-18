import os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import requests
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity

from config import BLOCKLIST, db
from middleware import verify_api_key
from models import UserModel, UserRegistrationModel
from schema import UserSchema, UserRegisterSchema
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
UserBlueprint = Blueprint(
    "Users", "users", description="Operations on users")


def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
        auth=("api", f"{os.getenv('MAILGUN_API_KEY')}"),
        data={
            "from": f"Taslim Arif <postmaster@{os.getenv('MAILGUN_DOMAIN')}>",
            "to": [to],
            "subject": subject,
            "text": body
        })


@UserBlueprint.route(f"/{os.getenv('API_VERSION')}/user/<string:user_id>")
class User(MethodView):
    jwt_required()

    @UserBlueprint.response(200, UserSchema)
    def get(self, user_id):
        try:
            user = UserModel.query.get_or_404(user_id)
            return user
        except SQLAlchemyError:
            return abort(
                404, message=f"User doesn't exist")
        except Exception as e:
            print(e)
            abort(
                500, message=f"An error occurred while getting the itemId {user_id}")

    # Needs token fetched from login not from refresh token
    @jwt_required(fresh=True)
    @UserBlueprint.response(204, None)
    def delete(self, user_id):
        try:
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}, 204
        except SQLAlchemyError:
            abort(
                500, message=f"An error occurred deleting the user {user_id}")
        except Exception as e:
            abort(500, message=f"An error occurred {e}")


@UserBlueprint.route(f"/{os.getenv('API_VERSION')}/register")
class UserRegister(MethodView):

    # @verify_x_api_key
    @UserBlueprint.arguments(UserRegisterSchema)
    @UserBlueprint.response(201, UserRegisterSchema)
    def post(self, user_data):
        try:
            if UserRegistrationModel.query.filter(
                or_(UserRegistrationModel.username == user_data['username'],
                    UserRegistrationModel.email == user_data['email'])
            ).first():
                abort(409, message='A user with that username or email already exists')
            username, password, email = user_data['username'], pbkdf2_sha256.hash(
                user_data['password']), user_data['email']

            user = UserRegistrationModel(
                username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            # But sending email might take  some time and we  don't want to interrupt user while we are sending emails. For this purpose we
            # will use redis and queue
            send_simple_message(
                to=user.email,
                subject='Successfully signed up',
                body=f'Hi {user.username}! You have successfully signed up to Stores API.'
            )
            return user
        except IntegrityError:
            abort(
                400,
                message="username already exists.",
            )
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="An error occurred creating the user.")


@UserBlueprint.route(f"/{os.getenv('API_VERSION')}/user")
class UserList(MethodView):

    jwt_required()

    @UserBlueprint.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@UserBlueprint.route(f"/{os.getenv('API_VERSION')}/login")
class UserLogin(MethodView):
    @UserBlueprint.arguments(UserSchema)
    @verify_api_key()
    def post(self, user_data):
        username = user_data['username']
        user = UserModel.query.filter(
            UserModel.username == username).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(
                identity=user.id, fresh=True, expires_delta=timedelta(days=1))
            refresh_token = create_refresh_token(
                identity=user.id, expires_delta=timedelta(days=90))
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid Credentials.")


@UserBlueprint.route(f"/{os.getenv('API_VERSION')}/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt().get('jti')
        BLOCKLIST.append(jti)  # TODO : Use redis or DB to maintain user token
        return {"message": "Logged Out Successfully"}

        """ 1. Token refreshing: 
            For security purposes, each access token must have an expiration time. Normally this is set to between 5 and 15 minutes, after which the user must re-authenticate.
            In Flask-JWT, the re-authentication would require the user to enter their username and password again. That can be very tedious for users!
            Token refreshing serves exactly this purpose. When authenticating via credentials the first time, we not only return an access token that contains the user's account info—we also return a refresh token that only serves to refresh the access token.
            When an access token has expired we provide the refresh token, and Flask-JWT-Extended verifies it and returns a new, valid access token. That way the user can keep using that access token for accessing the protected services.
            This process repeats every time the original access token expires... So does this mean the user never has to enter their credentials again?
            
            2. Token Freshness:
            Given the above description, one may ask what is the difference between using the token refreshing workflow and having an access token that never expires?
            It is true that it does not make a difference if we simply allow token refreshing with no further restrictions. However, there is a solution to make our authentication workflow more robust.
            Here's a common use case: once we've signed in, we are normally able to continue using an app without entering credentials. However, if we try to perform a "critical" operation—such deleting some data or completing a bank transaction—we are often asked for the credentials (or at least a password).
            How does that work?
            Enter, token freshness. As a rule of thumb, any access token acquired via credentials is marked as fresh, while access tokens acquired via the refresh mechanism are marked as non-fresh.
            Going back to our previous authentication workflow, the first time a user logs in with his credentials, he would get a fresh access token and a refresh token. If he tries to log back in and finds out his current access token has expired, he uses his refresh token to get a new access token. This new access token would be non-fresh, since it's not acquired with credentials.
            We still have some trust in the user when he presents the non-fresh access token. However, when he tries to perform a critical action, such as a transaction, the application would not accept this access token. Instead, he would need to enter his credentials again and get a new fresh access token to proceed with the critical action.
            Returns:
                _type_: _description_
        """


@UserBlueprint.route(f"/{os.getenv('API_VERSION')}/refresh")
class RefreshToken(MethodView):
    # Means it needs refresh token not access token
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}
