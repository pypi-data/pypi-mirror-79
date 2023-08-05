
class Users:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def CurrentUser(self):
        return self._connection.get(url='/users/whoami')
    def describe(self, id):
        return self._connection.get(url='/users/{id}'.format(id))
    def list(self):
        return self._connection.get(url='/users')
    def invite(self, data):
        return self._connection.post(url='/users', payload=data)
    def AddSSOUser(self, data):
        return self._connection.post(url='/users/sso', payload=data)
    def update(self, id, data):
        return self._connection.patch(url='/users/{id}'.format(id), payload=data)
    def revoke(self, id):
        return self._connection.delete(url='/users/{id}'.format(id))
