from flask import Blueprint
from flask import request, make_response
from apps import db
from apps.orm import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from .fake_data import fake_results
from .engine import engine_instance


user_blue = Blueprint('users', __name__, url_prefix='/user')


def safe_access(data, key, default):
    if not isinstance(data, dict): return
    if key not in data.keys(): return default
    else: return data[key]


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
    
    print('found', user.count(), user.first().username)
    
    if user.count() > 0:
        return make_response({'proceed': True, 'user': user.first().username}, 200)
    else:
        return make_response({'proceed': False}, 200)


@user_blue.route('/login_username', methods=['POST'])
def login_username():
    print('login username')
    data = request.get_json()
    
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username, password=password)
    # breakpoint()
    print('found', user.count())
    
    if user.count() > 0:
        return make_response({'proceed': True, 'email': user.first().email}, 200)
    else:
        return make_response({'proceed': False}, 200)
    
    
@user_blue.route('/subscribe', methods=['POST'])
def subsribe():
    print('subscribe')
    
    data = request.get_json()
    
    user = data['username']
    email = data['email']
    link = data['link']
    price = data['price']
    platform = data['platform']
    
    if not isinstance(price, str):
        print(f'price is not a string but rather {price}, setting it to a large number')
        price = '1000000'
    
    try:
        price = float(price)
    except:
        print(f'price cannot be converted to float [price: {price}], setting it to a large number')
        price = 1e6
        
    print(price, link, email, platform)
    
    ret = engine_instance.subscribe(price, link, user, email, platform)
    
    return make_response({'success': ret}, 200)


@user_blue.route('/search', methods=['POST'])
def search():
    print('search')
    data = request.get_json()
    query = data['query']  # query string
    
    # first see if in database
    cache = Cache.query.filter_by(search_name=query)
    
    if cache.count() > 0:
        respond = {'results': []}
        
        for row in cache:
            tmp = {
                'name': row.name,
                'class': row.class_,
                'size': Cache.to_list(row.size),
                'image': row.image,
                'link': row.link,
                'price': row.price,
                'history_price': Cache.to_pts_list(row.history_price),
                'platform': row.platform,
            }

            respond['results'].append(tmp)
    
    else:
        respond = engine_instance.search(query)

        for row in respond['results']:
            new_row = Cache(
                search_name=query,
                name=row['name'],
                class_=row['class'],
                size=Cache.to_str(row['size']),
                image=row['image'],
                link=row['link'],
                platform=row['platform'],
                price=row['price'],
                history_price=Cache.to_str(row['history_price']),
            )
            db.session.add(new_row)
            db.session.commit()
            print("Row added successfully.")
    
    return make_response(respond, 200)
