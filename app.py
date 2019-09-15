from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from db import db
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello world!'

@app.route('/data', methods = ['GET'])
def data():
	para = request.args.get('moviename')
	outputlist = []
	data2017 = db.readdb('db/moviescore2017.csv', para)
	data2018 = db.readdb('db/moviescore2018.csv', para)
	data2019 = db.readdb('db/moviescore2019.csv', para)
	outputlist.extend(data2017+data2018+data2019)
	return jsonify(outputlist)

@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')
	
if __name__ == '__main__':
    app.run(debug=True)