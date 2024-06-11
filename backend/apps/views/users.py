from flask import Blueprint
from flask import request, make_response
from apps import db
from apps.orm import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .llm import lm

user_blue = Blueprint('users', __name__, url_prefix='/user')

def get_course_comments():
    course_comments = []
    for course in Course.query.all():
        for comment in course.comments:
            course_comments.append((course.c_name, comment.content))
    return course_comments

def recommend(req):
    # get all course comment pairs
    cc_pairs = get_course_comments()
    cc_s = ''
    for pair in cc_pairs:
        cc_s += ' '
        cc_s += 'Course: ' + pair[0] + ' Comment: ' + pair[1]
    rt = lm.forward_text(user_msg=f'这是一些课程的名字和评论，请根据他们和需求推荐一门课，用全中文回答，英文评论也翻译成中文，不要出现英语字母。这是需求： {req}。 这是课程名与评论：' + cc_s,
                         system_msg='请用中文回答.')
    print(rt)
    return rt

def _add_course_comment(course_name, content, rating):  
    course = Course.query.filter_by(c_name=course_name).first()
    if course:
        new_comment = Comment(c_id=course.c_id, content=content, rating=rating)
        db.session.add(new_comment)
        db.session.commit()
        return True
    else:
        return False
    
def _add_teacher_comment(t_name, content, rating):
    new_comment = TeacherComment(t_name=t_name, content=content, rating=rating)
    db.session.add(new_comment)
    db.session.commit()
    return True

def _get_course_and_comments():
    courses = Course.query.all()
    result = []
    for course in courses:
        course_data = {
            'id': course.c_id,
            'code': course.c_code,
            'name': course.c_name,
            'credits': str(course.c_credits),
            'category': course.c_category,
            'department': course.c_department,
            'reviews': []
        }
        for comment in course.comments:
            course_data['reviews'].append([comment.rating, comment.content])
        result.append(course_data)
    return result

@user_blue.route('/add_teacher_comment', methods=['POST']) # 登录路由，向 /user/login 发送请求则会被此函数捕获
def add_teacher_comment():
    reqData = request.get_json() # 获取请求数据
    _add_teacher_comment(reqData['teacher'], reqData['review'], reqData['rating'])
    print(reqData)
    dict0 = {}
    dict0["status"] = 0
    dict0["resp"] = "Add teacher comment success!"
    # dict0["token"] = user_token
    return make_response(dict0, 200)

@user_blue.route('/get_recommend', methods=['POST'])
def get_recommend():
    reqData = request.get_json() # 获取请求数据
    req = reqData['req']
    # print('!!!!!!',req)
    result = recommend(req)
    dic = {'result': result}
    return make_response(dic, 200)

@user_blue.route('/get_course', methods=['GET'])
@jwt_required() # 需要请求携带 jwt ，即表明已登录状态
def get_course():
    dict0 = _get_course_and_comments()
    return make_response(dict0, 200)
