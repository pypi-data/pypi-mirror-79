
class ReportConfigs:
    def __init__(self, config, connection):
        self._config = config
        self._connection = connection
    def create(self, data):
        return self._connection.post(url='/report-configs', payload=data)
    def list(self, accountID, groupID):
        params = {}
        if accountID:
            params['accountId'] = accountID
        if groupID:
            params['groupId'] = accountID
        return self._connection.get(url='/report-configs',params=params)
    def describe(self, id):
        return self._connection.get(url='/report-configs/{id}'.format(id=id))
    def update(self, id, data):
        return self._connection.patch(url='/report-configs/{id}'.format(id=id), payload=data)
    def delete(self, id):
        return self._connection.delete(url='/report-configs/{id}'.format(id=id))
    