#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Computers:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
        self._epxand = ["none", "all", "computerStatus", "tasks", "securityUpdates", "computerSettings",
                        "allSecurityModules", "antiMalware", "webReputation", "activityMonitoring", "firewall",
                        "intrusionPrevention", "integrityMonitoring", "logInspection", "applicationControl", "SAP",
                        "interfaces", "ESXSummary", "allVirtualMachineSummaries", "azureARMVirtualMachineSummary",
                        "azureVMVirtualMachineSummary", "ec2VirtualMachineSummary", "noConnectorVirtualMachineSummary",
                        "vmwareVMVirtualMachineSummary", "vcloudVMVirtualMachineSummary", "workspaceVirtualMachineSummary",
                        "gcpVirtualMachineSummary"]
    def _processExpands(self, expands):
        rtv = []
        split = expands.split(",")
        for expand in split:
            added=False
            lowerCase = expand.lower()
            for ex in self._epxand:
                if ex.lower() == lowerCase:
                    rtv.append(ex)
                    added = True
                    break
            if not added:
                ##Unknown expands - maybe newer than SDK?
                rtv.append(expand)
        return rtv

    ##Computers
    def list(self, expand=None, overrides=None):
        params = {}
        if expand:
            params['expand'] = self._processExpands(expands=expand)
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers', params=params)
    def describe(self, id, expand=None, overrides=None):
        params = {}
        if expand:
            params['expand'] = self._processExpands(expands=expand)
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}'.format(computerID=id), params=params)
    def modify(self, id, expand=None, overrides=None, payload=None):
        params = {}
        if expand:
            params['expand'] = self._processExpands(expands=expand)
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}'.format(computerID=id), data=payload, params=params)
    def delete(self, id):
        return self._connection.delete(url='/computers/{computerID}'.format(computerID=id))
    def describeSetting(self, id, setting, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/settings/{name}'.format(computerID=id, name=setting), params=params)
    def modifySetting(self, id, setting, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/settings/{name}'.format(computerID=id, name=setting), data=payload, params=params)
    def resetSetting(self, id, setting, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/settings/{name}'.format(computerID=id, name=setting), params=params)
    def create(self, expand=None, overrides=None, payload=None):
        params = {}
        if expand:
            params['expand'] = expand
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers' , data=payload, params=params)
    def search(self, expand=None, overrides=None, payload=None):
        computers = None
        params = {}
        if expand:
            params['expand'] = self._processExpands(expands=expand)
        if overrides:
            params['overrides'] = overrides
        rtv = self._connection.post(url='/computers/search', data=payload, params=params)
        if 'computers' not in rtv:
            return rtv
        computers = rtv['computers']
        while len(rtv['computers']) > 0:
            if 'idTest' in payload['searchCriteria'][0]:
                if payload['searchCriteria'][0]['idTest'] == 'equal' or payload['searchCriteria'][0]['idTest'] == 'not-equal':
                    return computers
                if payload['searchCriteria'][0]['idTest'] == 'greater-than-or-equal':
                    payload['searchCriteria'][0]['idValue'] = int(computers[len(computers) - 1]['ID']) + 1
                if payload['searchCriteria'][0]['idTest'] == 'less-than-or-equal':
                    payload['searchCriteria'][0]['idValue'] = int(computers[len(computers) - 1]['ID']) - 1
                if payload['searchCriteria'][0]['idTest'] == 'less-than' or payload['searchCriteria'][0]['idTest'] == 'greater-than':
                    payload['searchCriteria'][0]['idValue'] = int(computers[len(computers) - 1]['ID'])
                rtv = self._connection.post(url='/computers/search', data=payload, params=params)
            computers.extend(rtv['computers'])
        return computers


    ##Computers Firewall Rule Assignments
    def listFirewallAssignment(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/firewall/assignments'.format(computerID=id), params=params)
    def addFirewallAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/firewall/assignments'.format(computerID=id), data=payload, params=params)
    def setFirewallAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.put(url='/computers/{computerID}/firewall/assignments'.format(computerID=id), data=payload, params=params)
    def deleteFirewallAssignment(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/firewall/assignments/{firewallRuleID}'.format(computerID=id, firewallRuleID=ruleID), params=params)
    ##Computers Firewall Rule
    def listFirewallRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/firewall/rules'.format(computerID=id), params=params)
    def describeFirewallRules(self, id, firewallRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/firewall/rules/{firewallRuleID}'.format(computerID=id, firewallRuleID=firewallRuleId), params=params)
    def modifyFirewallRules(self, id, firewallRuleId, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/firewall/rules/{firewallRuleID}'.format(computerID=id, firewallRuleID=firewallRuleId), data=payload, params=params)
    def resetFirewallRules(self, id, firewallRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/firewall/rules/{firewallRuleID}'.format(computerID=id, firewallRuleID=firewallRuleId), params=params)
    #IntegrityMonitoring
    def listIntegrityMonitoringRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/integritymonitoring/rules'.format(computerID=id), params=params)
    def describeIntegrityMonitoringRules(self, id, integritymonitoringlRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/integritymonitoring/rules/{integrityMonitoringRuleID}'.format(computerID=id, integrityMonitoringRuleID=integritymonitoringlRuleId), params=params)
    def modifyIntegrityMonitoringRules(self, id, integritymonitoringlRuleId, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/integritymonitoring/rules/{integrityMonitoringRuleID}'.format(computerID=id, integrityMonitoringRuleID=integritymonitoringlRuleId), data=payload, params=params)
    def deleteIntegrityMonitoringRules(self, id, integritymonitoringlRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/integritymonitoring/rules/{integrityMonitoringRuleID}'.format(computerID=id, integrityMonitoringRuleID=integritymonitoringlRuleId), params=params)

    # IntegrityMonitoring Assignments
    def listIntegrityMonitoringAssignments(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/integritymonitoring/assignments'.format(computerID=id), params=params)
    def setIntegrityMonitoringAssignments(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.put(url='/computers/{computerID}/integritymonitoring/assignments'.format(computerID=id), data=payload,params=params)
    def addIntegrityMonitoringAssignments(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/integritymonitoring/assignments'.format(computerID=id), data=payload,params=params)
    def deleteIntegrityMonitoringAssignments(self, id, integritymonitoringlRuleId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/integritymonitoring/assignments/{integrityMonitoringRuleID}'.format(computerID=id, integrityMonitoringRuleID=integritymonitoringlRuleId), params=params)
    #Intrusion Prevention - assignments
    def listIntrusionPreventionAssignment(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/intrusionprevention/assignments'.format(computerID=id), params=params)
    def assignIntrusionPreventionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/intrusionprevention/assignments'.format(computerID=id), data=payload, params=params)
    def createIntrusionPreventionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.put(url='/computers/{computerID}/intrusionprevention/assignments'.format(computerID=id), data=payload, params=params)
    def deleteComputerIntrusionPreventionAssignment(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/intrusionprevention/assignments/{intrusionPreventionRuleID}'.format(computerID=id, intrusionPreventionRuleID=ruleID), params=params)
    #Intrusion Prevention - application type
    def listIntrusionPreventionApplicationTypes(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/intrusionprevention/applicationtypes'.format(computerID=id), params=params)
    def describeIntrusionPreventionApplicationTypes(self, id, intrusionPreventionApplicationTypesId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/intrusionprevention/applicationtypes/{applicationTypeID}'.format(computerID=id, applicationTypeID=intrusionPreventionApplicationTypesId), params=params)
    def modifyIntrusionPreventionApplicationTypes(self, id, intrusionPreventionApplicationTypesId, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/intrusionprevention/applicationtypes/{applicationTypeID}'.format(computerID=id, applicationTypeID=intrusionPreventionApplicationTypesId), data=payload, params=params)
    def deleteIntrusionPreventionApplicationTypes(self, id, intrusionPreventionApplicationTypesId, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/intrusionprevention/applicationtypes/{applicationTypeID}'.format(computerID=id, applicationTypeID=intrusionPreventionApplicationTypesId), params=params)
    #Intrusion Prevention - Rule
    def listIntrusionPreventionRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/intrusionprevention/rules'.format(computerID=id), params=params)
    def describeIntrusionPreventionRule(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/intrusionprevention/rules/{intrusionPreventionRuleID}'.format(computerID=id, intrusionPreventionRuleID=ruleID), params=params)
    def modifyIntrusionPreventionRule(self, id, ruleID, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/intrusionprevention/rules/{intrusionPreventionRuleID}'.format(computerID=id, intrusionPreventionRuleID=ruleID), data=payload, params=params)
    def deleteIntrusionPreventionRules(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/intrusionprevention/rules/{intrusionPreventionRuleID}'.format(computerID=id, intrusionPreventionRuleID=ruleID), params=params)
    #Log Inspection assignment
    def listLogInspectionAssignment(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/loginspection/assignments'.format(computerID=id), params=params)
    def assignLogInspectionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/loginspection/assignments'.format(computerID=id), params=params, data=payload)
    def setLogInspectionAssignment(self, id, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.put(url='/computers/{computerID}/loginspection/assignments'.format(computerID=id), params=params, data=payload)
    def deleteLogInspectionAssignment(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/loginspection/assignments/{logInspectionRuleID}'.format(computerID=id, logInspectionRuleID=ruleID), params=params)
    #ILog Inspection  - rules
    def listLogInspectionRules(self, id, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/loginspection/rules'.format(computerID=id), params=params)
    def describeLogInspectionRule(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.get(url='/computers/{computerID}/loginspection/rules/{logInspectionRuleID}'.format(computerID=id, logInspectionRuleID=ruleID), params=params)
    def modifyLogInspectionRule(self, id, ruleID, overrides=None, payload=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/computers/{computerID}/loginspection/rules/{logInspectionRuleID}'.format(computerID=id, logInspectionRuleID=ruleID), data=payload, params=params)
    def deleteLogInspectionRule(self, id, ruleID, overrides=None):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.delete(url='/computers/{computerID}/loginspection/rules/{logInspectionRuleID}'.format(computerID=id, logInspectionRuleID=ruleID), params=params)



