from flask import Flask, request, render_template, session, jsonify
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.users

app = Flask(__name__)
app.secret_key = 'asdfgh123'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']

        new_user = {'id': id_receive, 'pw': pw_receive}
        # print(new_user)
        db.users.insert_one(new_user)
        # db.session.add(new_user)
        # db.session.commit()
        return jsonify({'result': 'success'})
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('cards.html')
    else:
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        try:
            user = db.users.find_one({'id': id_receive}, {'pw': pw_receive})
            if user is not None:
                session['logged_in'] = True
                return render_template('cards.html')
            else:
                return render_template('index.html')
        except:
            return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



