from flask import Flask, request, render_template, session, jsonify
from pymongo import MongoClient

# dddddd

client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)
app.secret_key = 'asdfgh123'


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']

        new_user = {'id': id_receive, 'pw': pw_receive}
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'result': 'success', 'msg': "회원가입 성공!"})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        try:
            user = db.users.find_one({'id': id_receive}, {'pw': pw_receive})
            if user is not None:
                session['logged_in'] = True
                return jsonify({'result': 'success', 'msg': "로그인 상태!"})
            else:
                return jsonify({'result': 'fail', 'msg': "로그아웃 상태!"})
        except:
            return jsonify({'result': 'fail', 'msg': "로그아웃 상태!"})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)