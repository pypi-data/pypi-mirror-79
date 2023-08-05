#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class ApplicationControl:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##ApplicationControl global rules
    def listGlobalRules(self):
        return self._connection.get(url='/applicationcontrolglobalrules')
    def createGlobalRule(self, payload):
        return self._connection.post(url='/applicationcontrolglobalrules', data=payload)
    def describeGlobalRule(self, ruleID):
        return self._connection.get(url='/applicationcontrolglobalrules/{ruleID}'.format(ruleID=ruleID))
    def modifyGlobalRule(self, ruleID, payload):
        return self._connection.post(url='/applicationcontrolglobalrules/{ruleID}'.format(ruleID=ruleID), data=payload)
    def deleteGlobalRule(self, ruleID):
        return self._connection.delete(url='/applicationcontrolglobalrules/{ruleID}'.format(ruleID=ruleID))
    def searchGlobalRules(self, payload):
        return self._connection.post(url='/applicationcontrolglobalrules/search', data=payload)
    ## ApplicationControl
    def listrulesets(self):
        return self._connection.get(url='/rulesets')
    def createruleset(self, payload):
        return self._connection.post(url='/rulesets', data=payload)
    def describeGlobalRule(self, rulesetID):
        return self._connection.get(url='/rulesets/{rulesetID}'.format(rulesetID=rulesetID))
    def modifyruleset(self, rulesetID, payload):
        return self._connection.post(url='/rulesets/{rulesetID}'.format(rulesetID=rulesetID), data=payload)
    def deleteruleset(self, rulesetID):
        return self._connection.delete(url='/rulesets/{rulesetID}'.format(rulesetID=rulesetID))
    def searchrulesets(self, payload):
        return self._connection.post(url='/rulesets/search', data=payload)
    def listrulesetRules(self, rulesetID):
        return self._connection.get(url='/rulesets/{rulesetID}/rules'.format(rulesetID=rulesetID))
    def describeRulesetRule(self, rulesetID, ruleID):
        return self._connection.get(url='/rulesets/{rulesetID}/rules/{ruleID}'.format(rulesetID=rulesetID,ruleID=ruleID))
    def modifyrulesetRule(self, rulesetID, ruleID, payload):
        return self._connection.post(url='/rulesets/{rulesetID}/rules/{ruleID}'.format(rulesetID=rulesetID,ruleID=ruleID), data=payload)
    def deleterulesetRule(self, rulesetID, ruleID):
        return self._connection.delete(url='/rulesets/{rulesetID}/rules/{ruleID}'.format(rulesetID=rulesetID,ruleID=ruleID))
    def searchrulesetRules(self, rulesetID, payload):
        return self._connection.post(url='/rulesets/{rulesetID}/rules/search'.format(rulesetID=rulesetID), data=payload)
    ## Software Changes
    def listsoftwareChanges(self):
        return self._connection.get(url='/softwarechanges')
    def describesoftwareChange(self, softwareChangeID):
        return self._connection.get(url='/softwarechanges/{softwareChangeID}'.format(softwareChangeID=softwareChangeID))
    def searchsoftwareChanges(self, payload):
        return self._connection.post(url='/softwarechanges/search', data=payload)
    def reviewSoftwareChange(self, payload):
        return self._connection.post(url='/softwarechanges/review', data=payload)
    ## Software Inventories
    def listSoftwareInventories(self):
        return self._connection.get(url='/softwareinventories')
    def createSoftwareInventory(self, payload):
        return self._connection.post(url='/softwareinventories', data=payload)
    def describeSoftwareInventory(self, softwareInventoryID):
        return self._connection.get(url='/softwareinventories/{softwareInventoryID}'.format(softwareInventoryID=softwareInventoryID))
    def deleteSoftwareInventory(self, softwareInventoryID):
        return self._connection.delete(url='/softwareinventories/{softwareInventoryID}'.format(softwareInventoryID=softwareInventoryID))
    def searchSoftwareInventory(self, payload):
        return self._connection.post(url='/softwareinventories/search', data=payload)
    def listSoftwareInventoryItems(self,softwareInventoryID):
        return self._connection.get(uurl='/softwareinventories/{softwareInventoryID}/items'.format(softwareInventoryID=softwareInventoryID))
    def searchSoftwareInventoryItems(self, softwareInventoryID, payload):
        return self._connection.post(url='/softwareinventories/{softwareInventoryID}/items/search'.format(softwareInventoryID=softwareInventoryID), data=payload)
    def describeSoftwareInventoryItem(self,softwareInventoryID, inventoryItemID):
        return self._connection.get(url='/softwareinventories/{softwareInventoryID}/items/{inventoryItemID}'.format(softwareInventoryID=softwareInventoryID, inventoryItemID=inventoryItemID))

