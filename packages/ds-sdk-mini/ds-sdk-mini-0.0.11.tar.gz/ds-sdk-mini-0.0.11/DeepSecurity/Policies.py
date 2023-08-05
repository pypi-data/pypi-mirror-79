#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

#import connect
#import config

class Policies:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Policies
    def list(self):
        return self._connection.get(url='/policies')
    def create(self, payload):
        return self._connection.post(url='/policies', data=payload)
    def describe(self, id):
        return self._connection.get(url='/policies/{policyID}'.format(id))
    def modify(self, id, payload):
        return self._connection.post(url='/policies/{policyID}'.format(id), data=payload)
    def delete(self, id):
        return self._connection.delete(url='/policies/{policyID}'.format(id))
    def search(self, overrides=False, payload=""):
        params = {}
        if overrides:
            params['overrides'] = overrides
        return self._connection.post(url='/policies/search', data=payload, params=params)
    # Default Policy Setting
    def describeDefaultSetting(self, name):
        return self._connection.get(url='/policies/default/settings/{name}'.format(name=name))
    def modifyDefaultSetting(self, name, payload):
        return self._connection.post(url='/policies/default/settings/{name}'.format(name=name), data=payload)
    def deleteDefaultSetting(self, name):
        return self._connection.delete(url='/policies/default/settings/{name}'.format(name=name))
    #Default Policy
    def listPolicyDefault(self):
        return self._connection.get(url='/policies/default')
    def modifyPolicyDefault(self, payload):
        return self._connection.post(url='/policies/default', data=payload)
    def describePolicyDefault(self, policyID, name):
        return self._connection.get(url='/policies/{policyID}/settings/{name}'.format(policyID=policyID, name=name))
    def modifyPolicySetting(self, policyID, name, payload):
        return self._connection.post(url='/policies/{policyID}/settings/{name}'.format(policyID=policyID, name=name), data=payload)
    def resetPolicySetting(self, policyID, name):
        return self._connection.delete(url='/policies/{policyID}/settings/{name}'.format(policyID=policyID, name=name))
    #Policy Firewall assignments
    def listFirewallRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/{policyID}/firewall/assignments'.format(policyID=str(policyID)))
    def AddFirewallRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/{policyID}/firewall/assignments'.format(policyID=policyID), data=payload)
    def SetFirewallRulesAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/{policyID}/firewall/assignments'.format(policyID=policyID), data=payload)
    def deleteFirewallRuleAssignments(self, policyID, firewallID):
        return self._connection.delete(url='/policies/{policyID}/firewall/assignments/{firewallRuleID}'.format(policyID=policyID, firewallRuleID=firewallID))
    # Policy Firewall
    def listFirewallRules(self, policyID):
        return self._connection.get(url='/policies/{policyID}/firewall/rules'.format(policyID=policyID))
    def describeFirewallRules(self, policyID, firewallID):
        return self._connection.get(url='/policies/{policyID}/firewall/rules/{firewallRuleID}'.format(policyID=policyID, firewallRuleID=firewallID))
    def modifyFirewallRules(self, policyID, firewallID, payload):
        return self._connection.post(url='/policies/{policyID}/firewall/rules/{firewallRuleID}'.format(policyID=policyID, firewallRuleID=firewallID), data=payload)
    def resetFirewallRules(self, policyID, firewallID):
        return self._connection.delete(url='/policies/{policyID}/firewall/rules/{firewallRuleID}'.format(policyID=policyID, firewallRuleID=firewallID))
    # Integrity monitoring assignments
    def listIntegrityMonitoringRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/{policyID}/integritymonitoring/assignments'.format(policyID=policyID))
    def addIntegrityMonitoringRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/{policyID}/integritymonitoring/assignments'.format(policyID=policyID), data=payload)
    def setIntegrityMonitoringRuleAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/{policyID}/integritymonitoring/assignments'.format(policyID=policyID), data=payload)
    def removeIntegrityMonitoringRuleAssignments(self, policyID, integritymonitoringID):
        return self._connection.delete(url='/policies/{policyID}/integritymonitoring/assignments/{integrityMonitoringRuleID}'.format(policyID=policyID, integrityMonitoringRuleID=integritymonitoringID))
    # Integrity monitoring
    def listIntegrityMonitoringRules(self, policyID):
        return self._connection.get(url='/policies/{policyID}/integritymonitoring/rules'.format(policyID=policyID))
    def describeIntegrityMonitoringRules(self, policyID, integritymonitoringID):
        return self._connection.get(url='/policies/{policyID}/integritymonitoring/rules/{integrityMonitoringRuleID}'.format(policyID=policyID, integrityMonitoringRuleID=integritymonitoringID))
    def modifyIntegrityMonitoringRules(self, policyID, integritymonitoringID, payload):
        return self._connection.post(url='/policies/{policyID}/integritymonitoring/rules/{integrityMonitoringRuleID}'.format(policyID=policyID, integrityMonitoringRuleID=integritymonitoringID), data=payload)
    def deleteIntegrityMonitoringRules(self, policyID, integritymonitoringID):
        return self._connection.delete(url='/policies/{policyID}/integritymonitoring/rules/{integrityMonitoringRuleID}'.format(policyID=policyID, integrityMonitoringRuleID=integritymonitoringID))
    # Intrusion Prevention assignments
    def listIntrusionPreventionRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/{policyID}/intrusionprevention/assignments'.format(policyID=policyID))
    def AddIntrusionPreventionRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/{policyID}/intrusionprevention/assignments'.format(policyID=policyID), data=payload)
    def SetIntrusionPreventionRulesAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/{policyID}/intrusionprevention/assignments'.format(policyID=policyID), data=payload)
    def deleteIntrusionPreventionRuleAssignments(self, policyID, intrusionpreventionID):
        return self._connection.delete(url='/policies/{policyID}/intrusionprevention/assignments/{intrusionPreventionRuleID}'.format(policyID=policyID, intrusionPreventionRuleID=intrusionpreventionID))
    # Intrusion Prevention
    def listIntrusionPreventionRules(self, policyID):
        return self._connection.get(url='/policies/{policyID}/intrusionprevention/rules'.format(policyID=policyID))
    def describeIntrusionPreventionRules(self, policyID, intrusionpreventionID):
        return self._connection.get(url='/policies/{policyID}/intrusionprevention/rules/{intrusionPreventionRuleID}'.format(policyID=policyID, intrusionPreventionRuleID=intrusionpreventionID))
    def modifyIntrusionPreventionRules(self, policyID, intrusionpreventionID, payload):
        return self._connection.post(url='/policies/{policyID}/intrusionprevention/rules/{intrusionPreventionRuleID}'.format(policyID=policyID, intrusionPreventionRuleID=intrusionpreventionID), data=payload)
    def resetIntrusionPreventionRules(self, policyID, intrusionpreventionID):
        return self._connection.delete(url='/policies/{policyID}/intrusionprevention/rules/{intrusionPreventionRuleID}'.format(policyID=policyID, intrusionPreventionRuleID=intrusionpreventionID))
    # Intrusion Prevention application
    def listIntrusionPreventionApplication(self, policyID):
        return self._connection.get(url='/policies/{policyID}/intrusionprevention/applicationtypes'.format(policyID=policyID))
    def describeIntrusionPreventionApplication(self, policyID, applicationID):
        return self._connection.get(url='/policies/{policyID}/intrusionprevention/applicationtypes/{applicationTypeID}'.format(policyID=policyID, applicationTypeID=applicationID))
    def modifyIntrusionPreventionApplication(self, policyID, applicationID, payload):
        return self._connection.post(url='/policies/{policyID}/intrusionprevention/applicationtypes/{applicationTypeID}'.format(policyID=policyID, applicationTypeID=applicationID), data=payload)
    def resetIntrusionPreventionApplication(self, policyID, applicationID):
        return self._connection.delete(url='/policies/{policyID}/intrusionprevention/applicationtypes/{applicationTypeID}'.format(policyID=policyID, applicationTypeID=applicationID))
    #Log inspection assignments
    def listLogInspectionRulesAssignments(self, policyID):
        return self._connection.get(url='/policies/{policyID}/loginspection/assignments'.format(policyID=policyID))
    def AddLogInspectionRuleAssignments(self, policyID, payload):
        return self._connection.post(url='/policies/{policyID}/loginspection/assignments'.format(policyID=policyID), data=payload)
    def SetLogInspectionRulesAssignments(self, policyID, payload):
        return self._connection.put(url='/policies/{policyID}/loginspection/assignments'.format(policyID=policyID), data=payload)
    def deleteLogInspectionRuleAssignments(self, policyID, loginspectionID):
        return self._connection.delete(url='/policies/{policyID}/loginspection/assignments/{logInspectionRuleID}'.format(policyID=policyID, logInspectionRuleID=loginspectionID))
    #Log Inspection
    def listLogInspection(self, policyID):
        return self._connection.get(url='/policies/{policyID}/loginspection/rules'.format(policyID=policyID))
    def describeLogInspection(self, policyID, applicationD):
        return self._connection.get(url='/policies/{policyID}/loginspection/rules/{logInspectionRuleID}'.format(policyID=policyID, logInspectionRuleID=applicationD))
    def modifyLogInspection(self, policyID, applicationD, payload):
        return self._connection.post(url='/policies/{policyID}/loginspection/rules/{logInspectionRuleID}'.format(policyID=policyID, logInspectionRuleID=applicationD), data=payload)
    def resetLogInspection(self, policyID, loginspectionID):
        return self._connection.delete(url='/policies/{policyID}/loginspection/rules/{logInspectionRuleID}'.format(policyID=policyID, logInspectionRuleID=applicationD))


