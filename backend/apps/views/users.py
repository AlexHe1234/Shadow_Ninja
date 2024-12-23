from flask import Blueprint
from flask import request, make_response
from apps import db
from apps.orm import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session


user_blue = Blueprint('users', __name__, url_prefix='/user')


def safe_access(data, key, default):
    if not isinstance(data, dict): return
    if key not in data.keys(): return default
    else: return data[key]

    
# @user_blue.route('/add_course_comment', methods=['POST']) # 登录路由，向 /user/login 发送请求则会被此函数捕获
# def add_course_comment():
#     reqData = request.get_json() # 获取请求数据
#     ret = _add_course_comment(reqData['course'], reqData['review'], reqData['rating'])
#     print(reqData)
#     dict0 = {}
#     if ret == True:
#         dict0["status"] = 0
#     else:
#         dict0["status"] = 1
#     dict0["resp"] = "Add course comment success!"
#     # dict0["token"] = user_token
#     return make_response(dict0, 200)


# @user_blue.route('/add_teacher_comment', methods=['POST']) # 登录路由，向 /user/login 发送请求则会被此函数捕获
# def add_teacher_comment():
    
#     reqData = request.get_json() # 获取请求数据
#     print(reqData)
    
#     _add_teacher_comment(reqData['teacher'], reqData['review'], reqData['rating'])
#     dict0 = {}
#     dict0["status"] = 0
#     dict0["resp"] = "Add teacher comment success!"
#     # dict0["token"] = user_token
#     return make_response(dict0, 200)


# @user_blue.route('/get_recommend', methods=['POST'])
# def get_recommend():
#     reqData = request.get_json() # 获取请求数据
#     req = reqData['req']
#     # print('!!!!!!',req)
#     result = recommend(req)
#     dic = {'result': result}
#     return make_response(dic, 200)


# @user_blue.route('/get_course', methods=['POST'])
# # @jwt_required() # 需要请求携带 jwt ，即表明已登录状态
# def get_course():
#     # print('hi')
#     dict0 = _get_course_and_comments()
#     print(dict0)
#     return make_response(dict0, 200)


# @user_blue.route('/get_summary', methods=['POST'])
# # @jwt_required() # 需要请求携带 jwt ，即表明已登录状态
# def get_summary():
#     # print('hi')
#     reqData = request.get_json() # 获取请求数据
#     res = _get_summary(reqData['course_name'])
#     dict0 = {'summary': res}
#     return make_response(dict0, 200)


# @user_blue.route('/get_teacher', methods=['POST'])
# # @jwt_required() # 需要请求携带 jwt ，即表明已登录状态
# def get_teacher():
#     # print('hi')
#     # reqData = request.get_json() # 获取请求数据
#     # res = _get_summary(reqData['course_name'])
#     res = _get_teacher()
#     dict0 = {'teacher': res}
#     return make_response(dict0, 200)

@user_blue.route('/register', methods=['POST'])
def register():
    print('register')
    data = request.get_json()    

    user_same_name = User.query.filter_by(username=safe_access(data, 'username', ''))
    email_same_name = User.query.filter_by(email=safe_access(data, 'email', ''))
    
    response = {
        'username': True,
        'email': True,
    }
    
    if user_same_name.count() > 0:
        response['username'] = False
    
    if email_same_name.count() > 0:
        response['email'] = False
    
    # register
    if response['email'] and response['username']:
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
        )
        db.session.add(new_user)
        db.session.commit()
    
    return make_response(response, 200)


@user_blue.route('/login_email', methods=['POST'])
def login_email():
    print('login email')
    data = request.get_json()
    
    email = data['email']
    password = data['password']
    
    user = User.query.filter_by(email=email, password=password)
    
    print('found', user.count())
    
    if user.count() > 0:
        return make_response({'proceed': True}, 200)
    else:
        return make_response({'proceed': False}, 200)


@user_blue.route('/login_username', methods=['POST'])
def login_username():
    print('login username')
    data = request.get_json()
    
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username, password=password)
    print('found', user.count())
    
    if user.count() > 0:
        return make_response({'proceed': True}, 200)
    else:
        return make_response({'proceed': False}, 200)
