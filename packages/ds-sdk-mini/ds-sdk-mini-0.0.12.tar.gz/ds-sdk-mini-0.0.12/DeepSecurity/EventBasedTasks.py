#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class EventBasedTasks:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##EventBasedTasks
    def list(self):
        return self._connection.get(url='/eventbasedtasks')
    def create(self, payload):
        return self._connection.post(url='/eventbasedtasks', data=payload)
    def search(self, payload):
        return self._connection.post(url='/eventbasedtasks/search', data=payload)
    def describe(self, eventbasedtaskID):
        return self._connection.get(url='/eventbasedtasks/{eventBasedTaskID}'.format(eventBasedTaskID=eventbasedtaskID))
    def modify(self, eventbasedtaskID, payload):
        return self._connection.post(url='/eventbasedtasks/{eventBasedTaskID}'.format(eventBasedTaskID=eventbasedtaskID), data=payload)
    def delete(self, eventbasedtaskID):
        return self._connection.delete(url='/eventbasedtasks/{eventBasedTaskID}'.format(eventBasedTaskID=eventbasedtaskID))
