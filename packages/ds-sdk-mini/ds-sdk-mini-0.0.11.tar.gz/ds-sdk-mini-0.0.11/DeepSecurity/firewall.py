#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class firewall:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Firewall rules
    def list(self):
        return self._connection.get(url='/firewallrules')
    def create(self, payload):
        return self._connection.post(url='/firewallrules', data=payload)
    def describe(self, firewallRuleID):
        return self._connection.get(url='/firewallrules/{firewallRuleID}'.format(firewallRuleID=firewallRuleID))
    def modify(self, firewallRuleID, payload):
        return self._connection.post(url='/firewallrules/{firewallRuleID}'.format(firewallRuleID=firewallRuleID), data=payload)
    def delete(self, firewallRuleID):
        return self._connection.delete(url='/firewallrules/{firewallRuleID}'.format(firewallRuleID=firewallRuleID))
    def search(self, payload):
        return self._connection.post(url='/firewallrules/search', data=payload)
    ##Interface Type
    def listInterfaceTypes(self, policyID):
        return self._connection.get(url='/policies/{policyID}/interfacetypes'.format(policyID=policyID))
    def createInterfaceType(self,policyID, payload):
        return self._connection.post(url='/policies/{policyID}/interfacetypes'.format(policyID=policyID), data=payload)
    def describeInterfaceType(self, policyID, interfaceTypeID):
        return self._connection.get(url='/policies/{policyID}/interfacetypes/{interfaceTypeID}'.format(policyID=policyID, interfaceTypeID=interfaceTypeID))
    def modifyInterfaceType(self, policyID, interfaceTypeID, payload):
        return self._connection.post(url='/policies/{policyID}/interfacetypes/{interfaceTypeID}'.format(policyID=policyID, interfaceTypeID=interfaceTypeID), data=payload)
    def deleteInterfaceType(self,  policyID, interfaceTypeID,):
        return self._connection.delete(url='/policies/{policyID}/interfacetypes/{interfaceTypeID}'.format(policyID=policyID, interfaceTypeID=interfaceTypeID))
    def searchInterfaceTypes(self, policyID, payload):
        return self._connection.post(url='/policies/{policyID}/interfacetypes/search'.format(policyID=policyID), data=payload)
    ##Firewall IP list
    def listIPLists(self):
        return self._connection.get(url='/iplists')
    def createiplists(self, payload):
        return self._connection.post(url='/iplists', data=payload)
    def describeIPList(self, ipListID):
        return self._connection.get(url='/iplists/{ipListID}'.format(ipListID))
    def modifyIPList(self, ipListID, payload):
        return self._connection.post(url='/iplists/{ipListID}'.format(ipListID), data=payload)
    def deleteIPList(self, ipListID):
        return self._connection.delete(url='/iplists/{ipListID}'.format(ipListID))
    def searchIPLists(self, payload):
        return self._connection.post(url='/iplists/search', data=payload)
    ##Firewall MAC list
    def listMacLists(self):
        return self._connection.get(url='/maclists')
    def createmaclists(self, payload):
        return self._connection.post(url='/maclists', data=payload)
    def describemacList(self, macListID):
        return self._connection.get(url='/maclists/{macListID}'.format(macListID=macListID))
    def modifymacList(self, macListID, payload):
        return self._connection.post(url='/maclists/{macListID}'.format(macListID=macListID), data=payload)
    def deletemacList(self, macListID):
        return self._connection.delete(url='/maclists/{macListID}'.format(macListID=macListID))
    def searchmacLists(self, payload):
        return self._connection.post(url='/maclists/search', data=payload)
    ##Firewall Port list
    def listPortLists(self):
        return self._connection.get(url='/portlists')
    def createportlists(self, payload):
        return self._connection.post(url='/portlists', data=payload)
    def describeportList(self, portListID):
        return self._connection.get(url='/portlists/{portListID}'.format(portListID=portListID))
    def modifyportList(self, portListID, payload):
        return self._connection.post(url='/portlists/{portListID}'.format(portListID=(portListID)), data=payload)
    def deleteportList(self, portListID):
        return self._connection.delete(url='/portlists/{portListID}'.format(portListID=portListID))
    def searchportLists(self, payload):
        return self._connection.post(url='/portlists/search', data=payload)
    ##Firewall Contexts
    def listContexts(self):
        return self._connection.get(url='/contexts')
    def createContext(self, payload):
        return self._connection.post(url='/contexts', data=payload)
    def describeContext(self, contextID):
        return self._connection.get(url='/contexts/{contextID}'.format(contextID=contextID))
    def modifyContext(self, contextID, payload):
        return self._connection.post(uurl='/contexts/{contextID}'.format(contextID=contextID), data=payload)
    def deleteContext(self, contextID):
        return self._connection.delete(url='/contexts/{contextID}'.format(contextID=contextID))
    def searchContexts(self, payload):
        return self._connection.post(url='/contexts/search', data=payload)
    ##Firewall Stateful Configurations
    def listStatefulConfigurations(self):
        return self._connection.get(url='/statefulconfigurations')
    def createStatefulConfiguration(self, payload):
        return self._connection.post(url='/statefulconfigurations', data=payload)
    def describeStatefulConfiguration(self, statefulConfigurationID):
        return self._connection.get(url='/statefulconfigurations/{statefulConfigurationID}'.format(statefulConfigurationID=statefulConfigurationID))
    def modifyStatefulConfiguration(self, statefulConfigurationID, payload):
        return self._connection.post(url='/statefulconfigurations/{statefulConfigurationID}'.format(statefulConfigurationID=statefulConfigurationID), data=payload)
    def deleteStatefulConfiguration(self, statefulConfigurationID):
        return self._connection.delete(url='/statefulconfigurations/{statefulConfigurationID}'.format(statefulConfigurationID=statefulConfigurationID))
    def searchStatefulConfigurations(self, payload):
        return self._connection.post(url='/statefulconfigurations/search', data=payload)



