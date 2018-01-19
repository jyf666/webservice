import requests


class Client:

    def __init__(self):
        self.response = requests.get(
            'http://192.168.227.144:8500/v1/agent/services'
        ).json().get('sqlite')
        self.address = self.response.get('Address')
        self.port = self.response.get('Port')

    def select_result(self, sql):
        try:
            students = requests.get(
                'http://{}:{}/{}'.format(self.address, self.port, sql)).json()
            for student in students:
                print(student[0])
            return 'success'
        except Exception as e:
            raise Exception("server offline")


if __name__ == '__main__':
    c = Client()
    c.select_result('select name from student_table')
