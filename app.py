from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from db import db
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello world!'

@app.route('/data', methods = ['GET'])
def data():
	para = request.args.get('moviename')
	outputlist = []
	for i in range (2007, 2020):
		dbdata=db.readdb('db/moviescorelist/moviescore'+str(i)+'.csv', para)
		outputlist.extend(dbdata)
	
	return jsonify(outputlist)

@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')
	
if __name__ == '__main__':
    app.run(debug=True)