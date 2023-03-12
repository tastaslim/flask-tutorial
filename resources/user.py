from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from config import BLOCKLIST, db
from models import UserModel
from schema import UserSchema
from passlib.hash import pbkdf2_sha256

UserBlueprint = Blueprint(
    "Users", "users", description="Operations on users")


@UserBlueprint.route("/user/<string:user_id>")
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

    @jwt_required()
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


@UserBlueprint.route("/register")
class UserRegister(MethodView):
    @UserBlueprint.arguments(UserSchema)
    @UserBlueprint.response(201, UserSchema)
    def post(self, user_data):
        try:
            username = user_data['username']
            password = pbkdf2_sha256.hash(user_data['password'])
            user = UserModel(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="username already exists.",
            )
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="An error occurred creating the user.")

        return user


@UserBlueprint.route("/user")
class UserList(MethodView):
    jwt_required()

    @UserBlueprint.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@UserBlueprint.route("/login")
class UserLogin(MethodView):
    @UserBlueprint.arguments(UserSchema)
    def post(self, user_data):
        username = user_data['username']
        user = UserModel.query.filter(
            UserModel.username == username).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            print(access_token)
            return {"access_token": access_token}
        abort(401, message="Invalid Credentials.")


@UserBlueprint.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt().get('jti')
        BLOCKLIST.append(jti)  # TODO : Use redis or DB to maintain user token
        return {"message": "Logged Out Successfully"}
