
class Profiles:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def list(self):
        return self._connection.get(url='/profiles')
    def describe(self, id):
        return self._connection.get(url='/profiles/{id}'.format(id=id))
    def create(self, data):
        return self._connection.post(url='/profiles', payload=data)
    def update(self, id, data):
        return self._connection.patch(url='/profiles/{id}'.format(id=id), payload=data)
    def delete(self, id):
        return self._connection.delete(url='/profiles/{id}'.format(id=id))
    def apply(self, id, data):
        return self._connection.post(url='/profiles/{id}/apply'.format(id=id), payload=data)