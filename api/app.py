#!flask/bin/python
from flask import Flask, jsonify, g
import sqlite3


app = Flask(__name__)

DATABASE = '/home/pi/Desktop/TemperatureConnected/temperatures.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@app.route('/temperatures', methods=['GET'])
def get_tasks():
    c = get_db().cursor()
    c.row_factory = dict_factory
    c.execute('''SELECT * FROM temperatures''')
    return jsonify(c.fetchall())

@app.route('/temperatures/v2.0', methods=['GET'])
def get_tasks_v2():
    c = get_db().cursor()
    c.row_factory = dict_factory
    c.execute('''SELECT * FROM temperatures_v2_1''')
    return jsonify(c.fetchall())

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
