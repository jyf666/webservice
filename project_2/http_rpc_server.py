from flask import Flask
from flask_jsonrpc import JSONRPC
import time
import json
import psutil

# Flask application
app = Flask(__name__)

# Flask-JSONRPC
jsonrpc = JSONRPC(app, '/', enable_web_browsable_api=True)


@jsonrpc.method('get_response')
def get_response(get_name):
    response_result = ""
    if(get_name == "time"):
        now = {"time": int(time.time())}
        response_result = json.dumps(now)
    elif(get_name == "ram"):
        mem = {"total": psutil.virtual_memory().total,
               "used": psutil.virtual_memory().used}
        response_result = json.dumps(mem)
    elif(get_name == "hdd"):
        hdd = {"total": psutil.disk_usage(
            '/').total, "used": psutil.disk_usage('/').used}
        response_result = json.dumps(hdd)
    return response_result


@jsonrpc.method('get_add')
def get_add(a, b):
    return json.dumps(a + b)


@jsonrpc.method('get_sub')
def get_sub(a, b):
    return json.dumps(a - b)


@jsonrpc.method('get_xml')
def get_xml(json_string):
    json_dict = json.loads(json_string)
    xml = []
    for k in sorted(json_dict.keys()):
        v = json_dict.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
