from flask import Flask
from flask import make_response
import time
import json
import psutil
#
app = Flask(__name__)
#


@app.route('/')
def hello_world():
    return 'Hello , My name is JYF!'


@app.route('/<get_name>', methods=['GET'])
def get_response(get_name):
    response_result = ""
    if(get_name == "time"):
        now = {"time": int(time.time())}
        response_result = json.dumps(now)
    elif(get_name == "ram"):
        mem = {"total": int(psutil.virtual_memory().total / 1024 / 1024),
               "used": int(psutil.virtual_memory().used / 1024 / 1024)}
        response_result = json.dumps(mem)
    elif(get_name == "hdd"):
        hdd = {"total": int(psutil.disk_usage('/').total / 1024 / 1024),
               "used": int(psutil.disk_usage('/').used / 1024 / 1024)}
        response_result = json.dumps(hdd)

    # 更改response header
    response_result = make_response(response_result)
    response_result.headers['Content-type'] = 'application/json'
    return response_result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8001)
