from flask_jsonrpc.proxy import ServiceProxy
import json


class Client:

    def __init__(self, server_addr):
        self.server_addr = server_addr
        self.server = ServiceProxy('http://' + server_addr + '/')

    def time(self):
        try:
            response = self.server.get_response('time').get('result')
            time_result = json.loads(response).get('time')
            return time_result
        except Exception as e:
            raise Exception("server offline")

    def ram(self):
        try:
            response = self.server.get_response('ram').get('result')
            total = int(json.loads(response).get('total'))
            used = int(json.loads(response).get('used'))
            return used, total
        except Exception as e:
            raise Exception("server offline")

    def hdd(self):
        try:
            response = self.server.get_response('hdd').get('result')
            total = int(json.loads(response).get('total'))
            used = int(json.loads(response).get('used'))
            return used, total
        except Exception as e:
            raise Exception("server offline")

    def add(self, a, b):
        if isinstance(a, int) and isinstance(b, int):
            try:
                response = self.server.get_add(a, b).get('result')
                response = int(json.loads(response))
                return response
            except Exception as e:
                raise Exception("server offline")
        else:
            raise Exception("invalid paramater")

    def sub(self, a, b):
        if isinstance(a, int) and isinstance(b, int):
            try:
                response = self.server.get_sub(a, b).get('result')
                response = int(json.loads(response))
                return response
            except Exception as e:
                raise Exception("server offline")
        else:
            raise Exception("invalid paramater")

    def json_to_xml(self, json_string):
        if(check_jsonstr(json_string)):
            try:
                response = self.server.get_xml(json_string).get('result')
                return response
            except Exception as e:
                raise Exception("server offline")
        else:
            raise Exception("invalid paramater")


def check_jsonstr(json_string):
    try:
        json.loads(json_string)
        return True
    except json.decoder.JSONDecodeError:
        return False


if __name__ == '__main__':
    c = Client('127.0.0.1:3000')
    print(c.time())
    print(c.ram())
    print(c.hdd())
    print(c.add(1, None))
    print(c.sub(1, 3))
    print(c.json_to_xml('{"message":"I am a JSON message"}'))
