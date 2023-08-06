
class APIKey:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    def list(self):
        return self._config.get(url='/api-keys')
    def describe(self, id):
        return self._config.get(url='/api-keys/{id}'.format(id=id))
