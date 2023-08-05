#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class gcpconnector:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection

    def createAction(self, id, payload):
        return self._connection.post(url='/gcpconnectors/{gcpConnectorID}/actions'.format(gcpConnectorID=id), data=payload)
    def describeAction(self, id, actionID):
        return self._connection.get(url='/gcpconnectors/{gcpConnectorID}/actions/{actionID}'.format(gcpConnectorID=id, actionID=actionID))
    def list(self):
        return self._connection.get(url='/gcpconnectors')
    def create(self, payload):
        return self._connection.post(url='/gcpconnectors', data=payload)
    def search(self, payload):
        return self._connection.post(url='/gcpconnectors/search', data=payload)
    def describe(self, id):
        return self._connection.get(url='/gcpconnectors/{gcpConnectorID}'.format(gcpConnectorID=id))
    def modify(self, id, payload):
        return self._connection.post(url='/gcpconnectors/{gcpConnectorID}'.format(gcpConnectorID=id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/gcpconnectors/{gcpConnectorID}'.format(gcpConnectorID=id))





