from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.week

db.users.insert_one({'name': 'bobby', 'age': 21})
db.users.insert_one({'name': 'kay', 'age': 27})
db.users.insert_one({'name': 'john', 'age': 30})


@app.route('/home')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
