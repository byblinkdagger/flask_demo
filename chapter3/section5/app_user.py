from flask import Flask, request, jsonify
from ext import db
from werkzeug.wrappers import Response

app = Flask(__name__)
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
    __tablename__ = 'users_learn'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    city = db.Column(db.String(50))
    token = db.Column(db.String(50))

    def __init__(self, name,password,city):
        self.name = name
        self.password = password
        self.city = city

class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    page = db.Column(db.Integer())
    price = db.Column(db.Integer())
    avator = db.Column(db.String(50))

    def __init__(self,name,page):
        self.user = user
        self.name = name
        self.page = page

class Records(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer())
    book_id = db.Column(db.Integer())
    name = db.Column(db.String(50))

    def __init__(self,user_id,book_id,name):
        self.user_id = user_id
        self.book_id = book_id
        self.name = name


with app.app_context():
    # db.drop_all()
    db.create_all()
    user = User('xiaoming', '123456','上海')
    user1 = User('keke', '123456','南京')
    db.session.add(user)
    db.session.add(user1)

    book1 = Books("十万个为什么",200)
    book2 = Books("雪中悍刀行",200)
    book3 = Books("白马出凉州",99)
    book4 = Books("江湖告急",100)
    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.add(book4)

    db.session.commit()

# query
@app.route('/users/',methods=['GET'])
def getUserInfo():

    id=request.args['id']
    if id:
        user = User.query.filter_by(id=id).first()
        return jsonify({
            'code':'0000',
            'data':{
                'id':user.id,
                'name':user.name,
                'password':user.password
            }
        })
    else:
        return jsonify({
            'code':'0101',
            'msg':'查无此人'
        })


# 登录
@app.route('/login/', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name).first()
    if user.password == password:
        token = name + password
        user.token = token
        db.session.commit()
        return str(token)
    else:
        return 'password not correct'

# 注册
@app.route('/register/', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')
    city = request.form.get('city')
    if (name and password and city) is None :
        return jsonify({
                'code':'0001',
                'msg':'信息不全'
            })
    else:
        user = User(name,password,city)
        print ('User ID: {}'.format(user.id))
        db.session.add(user)
        db.session.commit()
        return jsonify({
                'code':'0000',
                'msg':'注册成功'
            })

# 借阅记录
@app.route('/books/records/', methods=['POST'])
def books():
    token = request.headers.get('token')
    user_id = request.form.get('id')
    user = User.query.filter_by(id=user_id).first()
    if user.token == token :
        records = Records.query.filter_by(user_id=user_id).all()
        data = []
        for record in records:
            data.append({
                'id':record.id,
                'name':record.name,
            })
        return jsonify({
            'code':'0000',
            'data':data
        })
    else:
        return jsonify({
            'code': '0001',
            'msg':'token illegal'
        })

# 借阅
@app.route('/books/borrow/', methods=['POST'])
def borrow_books():
    user_id = request.form.get('user_id')
    book_id = request.form.get('book_id')
    book = Books.query.filter_by(id=book_id).first()
    if book:
        record = Records(user_id,book_id,book.name)
        db.session.add(record)
        db.session.commit()
        return jsonify({
                'code': '0000',
                'msg':'borrow success'
            })
    else:
        return jsonify({
                'code': '0001',
                'msg':'id illegal'
            })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000,debug = True)