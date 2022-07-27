from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:1234@cluster0.9i5vz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

#==============hy===============#

@app.route('/hy')
def hy():
    return render_template('hy.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    now = datetime.now()
    name_receive = request.form['name_give']
    post_receive = request.form['post_give']

    doc = {
        'name':name_receive,
        'post':post_receive,
        'year':now.year,
        'month':now.month,
        'day':now.day,
        'hour': now.hour,
        'minute': now.minute
    }
    db.post.insert_one(doc)

    return jsonify({'msg': '남기기 성공!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    post_list = list(db.post.find({}, {'_id': False}))
    return jsonify({'post': post_list})
#==============hy===============#

#==============bucket===============#

@app.route('/buc')
def bucket():
    return render_template('bucket.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list)+1

    doc = {

        'num':count,
        'bucket':bucket_receive,
        'done':0

    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '완료 되었습니다!'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)}, {'$set': {'done': 0}})

    return jsonify({'msg': '취소 되었습니다!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))

    return jsonify({'bucket':bucket_list})





#==============bucket===============#













if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)