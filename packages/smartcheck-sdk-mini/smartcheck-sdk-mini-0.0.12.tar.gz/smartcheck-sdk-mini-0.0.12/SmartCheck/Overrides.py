#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Overrides:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection

    def listVulnerabilityFindingOverrides(self, limit=25, query=None):
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url='/api/overrides/vulnerabilities', params=params)
        items = rtv['overrides']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url='/api/overrides/vulnerabilities', params=params)
            items.extend(rtv['overrides'])
        return items
    def createVulnerabilityFindingOverride(self, payload):
        return self._connection.post(url='/api/overrides/vulnerabilities', data=payload)
    def describeVulnerabilityFindingOverride(self, id):
        return self._connection.get(url='/api/overrides/vulnerabilities/{id}'.format(id=id))
    def modifyVulnerabilityFindingOverride(self, id, payload):
        return self._connection.post(url='/api/overrides/vulnerabilities/{id}'.format(id=id), data=payload)
    def deleteVulnerabilityFindingOverride(self, id):
        return self._connection.delete(url='/api/overrides/vulnerabilities/{id}'.format(id=id))
    def listContentFindingOverrides(self, limit=25, query=None):
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url='/api/overrides/contents', params=params)
        items = rtv['overrides']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url='/api/overrides/contents', params=params)
            items.extend(rtv['overrides'])
        return items
    def createContentFindingOverride(self, payload):
        return self._connection.post(url='/api/overrides/contents', data=payload)
    def describeContentFindingOverride(self, id):
        return self._connection.get(url='/api/overrides/contents/{id}'.format(id=id))
    def modifyContentFindingOverride(self, id, payload):
        return self._connection.post(url='/api/overrides/contents/{id}'.format(id=id), data=payload)
    def deleteContentFindingOverride(self, id):
        return self._connection.delete(url='/api/overrides/contents/{id}'.format(id=id))
    def listChecklistFindingOverrides(self, limit=25, query=None):
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url='/api/overrides/checklists', params=params)
        items = rtv['overrides']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url='/api/overrides/checklists', params=params)
            items.extend(rtv['overrides'])
        return items
    def createChecklistFindingOverride(self, payload):
        return self._connection.post(url='/api/overrides/checklists', data=payload)
    def describeChecklistFindingOverride(self, id):
        return self._connection.get(url='/api/overrides/checklists/{id}'.format(id=id))
    def modifyChecklistFindingOverride(self, id, payload):
        return self._connection.post(url='/api/overrides/checklists/{id}'.format(id=id), data=payload)
    def deleteChecklistFindingOverride(self, id):
        return self._connection.delete(url='/api/overrides/checklists/{id}'.format(id=id))




