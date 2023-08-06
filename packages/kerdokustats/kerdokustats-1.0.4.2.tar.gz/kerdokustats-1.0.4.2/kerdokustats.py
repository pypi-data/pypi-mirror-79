import requests

class kerdoku:
    def __init__(self):
        self.__r = requests.get('http://smartcat1908.pythonanywhere.com/todo/api/v1.0/tasks')

    def get_guilds(self):
        self.result = self.__r.json()["info"]['guilds']
        return self.result

    @property
    def guilds(self):
        return self.get_guilds()

    def get_users(self):
        self.result = self.__r.json()["info"]['users']
        return self.result

    @property
    def users(self):
        return self.get_users()

    def get_time(self):
        self.result = self.__r.json()["info"]['time']
        return self.result

    @property
    def time(self):
        return self.get_time()