from models import UserModel, UserRegistrationModel


def test_new_user():
    """
        Given a User Registration model WHEN a new User is created THEN check the email, password, and username fields are defined correctly
    """
    user = UserRegistrationModel(
        email='taslimarif@gmail.com', password='FlaskIsAwesome', username='username')
    assert user.email == 'taslimarif@gmail.com'
    assert user.password == 'FlaskIsAwesome'
    assert user.username == 'username'
