from datetime import timedelta

from bs4 import BeautifulSoup
from flask import Flask, request, render_template, session, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from pip._vendor import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'asdfgh123'


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        pw2_receive = request.form['pw2_give']

        user = db.users.find_one({'id': id_receive})

        if user is not None or pw_receive != pw2_receive:
            return jsonify({'result': 'fail'})
        else:
            pw_hash = bcrypt.generate_password_hash(pw_receive)
            new_user = {'id': id_receive, 'pw': pw_hash}
            # print(new_user)
            db.users.insert_one(new_user)
            return jsonify({'result': 'success'})


@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    user = db.users.find_one({'id': id_receive})

    if user is not None:
        user_pw = user['pw']
        check_pw = bcrypt.check_password_hash(user_pw, pw_receive)

        if check_pw is True:
            session['user'] = id_receive
            return jsonify({'result': 'success'})
        else:
            return jsonify({'result': 'fail'})
    else:
        return jsonify({'result': 'fail'})


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('home'))


@app.route('/card')
def card():
    if 'user' in session:
        # 로그인 상태가 아닐 경우 (세션에 user가 없을 경우)
        return render_template('cards.html')
    return redirect(url_for('home'))


@app.route('/show', methods=['GET'])
def show_gourmet():
    result = list(db.gourmet.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'gourmet': result})


@app.route('/post/like', methods=['POST'])
def like_gourmet():
    name_receive = request.form['name_give']

    gourmet = db.gourmet.find_one({'name': name_receive})
    new_like = gourmet['like'] + 1
    db.gourmet.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success'})


@app.route('/post/delete', methods=['POST'])
def delete_gourmet():
    name_receive = request.form['name_give']

    db.gourmet.delete_one({'name': name_receive})
    return jsonify({'result': 'success'})


@app.route('/post', methods=['POST'])
def post_gourmet():
    # 1. 클라이언트로부터 데이터를 받기
    name_receive = request.form['name_give']  # 클라이언트로부터 이름을 받는 부분
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분

    # 3. mongoDB에 데이터를 넣기

    # 타겟 URL을 읽어서 HTML를 받아오고,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # name = soup.select_one('#og\:title')
    imgurl = soup.select_one('#og\:image')['content']
    # tmp = soup.select_one('place_thumb')
    # imgurl = tmp.find('img')

    # print(tmp)  # HTML을 받아온 것을 확인할 수 있다.

    gourmet = {
        'name': name_receive,
        'imgurl': imgurl,
        'like': 0
    }

    db.gourmet.insert_one(gourmet)

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
