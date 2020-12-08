
from flask import Flask, render_template, jsonify, request

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_memo():
    # 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분
    key_receive = request.form['key_give']
    ver2 = {
        'title': title_receive, 'comment': comment_receive, 'key': key_receive
    }

    # 3. mongoDB에 데이터를 넣기
    db.ver2.insert_one(ver2)

    return jsonify({'result': 'success'})


@app.route('/memo/update', methods=['POST'])
def update_memo():
    # 1. 클라이언트로부터 데이터를 받기
    print('성공!')
    title_receive = request.form['title_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분
    key_receive = request.form['key_give']

    db.ver2.update_one({'key': key_receive}, {'$set': {'title': title_receive}})
    db.ver2.update_one({'key': key_receive}, {'$set': {'comment': comment_receive}})

    # 3. mongoDB에 데이터를 넣기
    return jsonify({'result': 'success'})


@app.route('/memo/delete', methods=['POST'])
def delete_memo():
    key_receive = request.form['key_give']
    print(key_receive)

    db.ver2.delete_one({'key': key_receive})

    return jsonify({'result': 'success'})


@app.route('/memo', methods=['GET'])
def read_memo():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.ver2.find({}, {'_id': 0}))
    print(result)
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'ver2': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)