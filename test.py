from flask import Flask, request, render_template, session, jsonify
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


@app.route('/')
def home():
    return render_template('cards.html')


@app.route('/show', methods=['GET'])
def show_gourmet():
    result = list(db.gourmet.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'gourmet': result})


@app.route('/post/like', methods=['POST'])
def like_gourmet():
    name_receive = request.form['name_give']

    gourmet = db.gourmet.find_one({'name': name_receive})
    new_like = gourmet['like']+1
    db.gourmet.update_one({'name': name_receive}, {'$set': {'like': new_like}})
    return jsonify({'result': 'success'})


@app.route('/post/delete', methods=['POST'])
def delete_gourmet():
    name_receive =request.form['name_give']

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