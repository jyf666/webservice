from flask import Flask
import sqlite3
import json

# Flask application
app = Flask(__name__)


@app.route('/health')
def hello_world():
    return 'Hello , success'


@app.route('/<sql>', methods=['GET'])
def select_sql(sql):
    response_result = ""
    conn = sqlite3.connect("testing_db.sql3")
    cursor = conn.cursor()

    cursor.execute(sql)
    response_result = cursor.fetchall()
    cursor.close()
    conn.commit()[]
    conn.close()
    return json.dumps(response_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)
