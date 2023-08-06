#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class AgentVersionControl:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##AgentVersionControl
    def describe(self, profileID):
        return self._connection.get(url='/agentversioncontrolprofiles/{agentVersionControlProfileID}/agentversioncontrols'.format(agentVersionControlProfileID=profileID))
    def modify(self, profileID, payload):
        return self._connection.post(url='/agentversioncontrolprofiles/{agentVersionControlProfileID}/agentversioncontrols'.format(agentVersionControlProfileID=profileID), data=payload)
    def search(self, profileID, payload):
        return self._connection.post(url='/agentversioncontrolprofiles/{agentVersionControlProfileID}/agentversioncontrols/search'.format(agentVersionControlProfileID=profileID), data=payload)
    def describeControl(self, profileID, agentVersionControlID):
        return self._connection.get(url='/agentversioncontrolprofiles/{agentVersionControlProfileID}/agentversioncontrols/{agentVersionControlID}'.format(agentVersionControlProfileID=profileID, agentVersionControlID=agentVersionControlID))
    def listProfiles(self):
        return self._connection.get(url='/agentversioncontrolprofiles')
    def describeProfile(self, profileID):
        return self._connection.get(url='/agentversioncontrolprofiles/{agentVersionControlProfileID}'.format(agentVersionControlProfileID=profileID))



