#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class IntrusionPrevention:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ## Application Types
    def listTypes(self):
        return self._connection.get(url='/applicationtypes')
    def createType(self, payload):
        return self._connection.post(url='/applicationtypes', data=payload)
    def createType(self, applicationTypeID):
        return self._connection.get(url='/applicationtypes/{applicationTypeID}'.format(applicationTypeID=applicationTypeID))
    def modifyType(self, applicationTypeID, payload):
        return self._connection.post(url='/applicationtypes/{applicationTypeID}'.format(applicationTypeID=applicationTypeID), data=payload)
    def deleteType(self, applicationTypeID):
        return self._connection.delete(url='/applicationtypes/{applicationTypeID}'.format(applicationTypeID=applicationTypeID))
    def searchTypes(self, payload):
        return self._connection.post(url='/applicationtypes/search', data=payload)
    ## Rules
    def listRules(self):
        return self._connection.get(url='/intrusionpreventionrules')
    def createRules(self, payload):
        return self._connection.post(url='/intrusionpreventionrules', data=payload)
    def describeRule(self, intrusionPreventionRuleID):
        return self._connection.get(url='/intrusionpreventionrules/{intrusionPreventionRuleID}'.format(intrusionPreventionRuleID=intrusionPreventionRuleID))
    def modifyRule(self, intrusionPreventionRuleID, payload):
        return self._connection.post(url='/intrusionpreventionrules/{intrusionPreventionRuleID}'.format(intrusionPreventionRuleID=intrusionPreventionRuleID), data=payload)
    def deleteRule(self, intrusionPreventionRuleID):
        return self._connection.delete(url='/intrusionpreventionrules/{intrusionPreventionRuleID}'.format(intrusionPreventionRuleID=intrusionPreventionRuleID))
    def searchRules(self, payload):
        return self._connection.post(url='/intrusionpreventionrules/search', data=payload)

