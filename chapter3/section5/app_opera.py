from functools import wraps

from ext import db
from flask import Flask, request, jsonify
from werkzeug.wrappers import Response
import redis
import hashlib
import time

app = Flask(__name__)
redis_store = redis.Redis(host='localhost', port=6379, password='123456')
app.config.from_object('config')
db.init_app(app)


class JSONResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSONResponse, cls).force_type(rv, environ)


app.response_class = JSONResponse


class User(db.Model):
    __tablename__ = 'users_opera'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))
    mobile = db.Column(db.String(50))
    movies = db.Column(db.String(200))

    def __init__(self, name, password, age, city, mobile, movies):
        self.name = name
        self.password = password
        self.age = age
        self.city = city
        self.mobile = mobile
        self.movies = movies


def login_check(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'code': '0001', 'message': '需要token验证'})

        mobile = token.split('&')[0]
        retoken = redis_store.get(mobile).decode(encoding = "utf-8")
        print(mobile)
        print(token)
        print(redis_store.get(mobile))
        print(not mobile)
        print(token != redis_store.get(mobile))
        if not mobile or token != retoken:
            return jsonify({'code': '0002', 'message': 'token信息错误'})

        return f(*args, **kwargs)

    return decorator

# 注册
@app.route('/register/', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')
    age = request.form.get('age')
    city = request.form.get('city')
    mobile = request.form.get('mobile')
    movies = request.form.get('movies')
    if (name and password and mobile) is None:
        return jsonify({
            'code': '0001',
            'msg': '信息不全'
        })
    else:
        exist = User.query.filter_by(mobile = mobile).first()
        if exist:
            return jsonify({
            'code': '0001',
            'msg': '该用户已注册'
        })
        else:
            user = User(name, password, age, city, mobile, movies)
            print('User ID: {}'.format(user.id))
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'code': '0000',
                'msg': '注册成功'
            })


# 登录
@app.route('/login/', methods=['POST'])
def login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    user = User.query.filter_by(mobile=mobile).first()
    if user is not None:
        if user.password == password:
            m = hashlib.md5()
            m.update(mobile.encode("utf8"))
            m.update(password.encode("utf8"))
            m.update(str(int(time.time())).encode("utf8"))
            token = m.hexdigest()
            redis_store.set(mobile,mobile+"&"+token)
            redis_store.expire(mobile,3600)
            return jsonify({
                'code': '0000',
                'token': mobile+"&"+token,
                'msg': '登录成功'
            })
        else:
            return jsonify({
                'code': '0001',
                'msg': '密码错误'
            })
    else:
        return jsonify({
            'code': '0001',
            'msg': '此用户暂无注册'
        })


@app.route('/user/', methods=['POST'])
@login_check
def getUser():
    token = request.headers.get('token')
    mobile = token.split('&')[0]
    user = User.query.filter_by(mobile=mobile).first()
    if user :
        return jsonify({
            'code': '0000',
            'data': {
                'id':user.id,
                'name':user.name,
                'age':user.age,
                'city':user.city,
                'mobile':user.mobile,
                'movies':user.movies
            },
            'msg': '成功'
        })
    else:
        return jsonify({
            'code': '0001',
            'msg': '暂无此用户信息'
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8829, debug=True)