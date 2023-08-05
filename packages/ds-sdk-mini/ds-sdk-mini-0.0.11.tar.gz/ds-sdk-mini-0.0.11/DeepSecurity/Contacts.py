#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Contacts:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Contacts
    def list(self):
        return self._connection.get(url='/contacts')
    def create(self, payload):
        return self._connection.post(url='/contacts', data=payload)
    def describe(self, contactID):
        return self._connection.get(url='/contacts/{contactID}'.format(contactID=contactID))
    def modify(self, contactID, payload):
        return self._connection.post(url='/contacts/{contactID}'.format(contactID=contactID), data=payload)
    def delete(self, contactID):
        return self._connection.delete(url='/contacts/{contactID}'.format(contactID=contactID))
    def search(self, payload):
        return self._connection.post(url='/contacts/search', data=payload)


