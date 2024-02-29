from flask import Blueprint, request
from flask_login import login_user
from werkzeug.security import generate_password_hash

from db_models import User, db

user_controller = Blueprint('user_controller', __name__, url_prefix='/user')


@user_controller.route('/registration', methods=['POST'])
def registration():
    data = request.get_json()
    if User.query.filter(User.email == str(data['email'])).first() != None:
        return 'Пользователь с таким email же был зарегистрирован', 409
    new_user = User(
        username=str(data['username']),
        email=str(data['email']),
        password=generate_password_hash(str(data['password']))
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return {
        'username': new_user.username
    }
