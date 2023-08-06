#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class ContentRules:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    def listContentRulesetCollections(self, limit=25, expand="all", query=None):
        params={'limit': limit, 'expand':expand}
        if query:
            params['query'] = query
        rtv = self._connection.get(url='/api/collections', params=params)
        items = rtv['collections']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url='/api/collections', params=params)
            items.extend(rtv['collections'])
        return items
    def createContentRulesetCollection(self, payload):
        return self._connection.post(url='/api/collections', data=payload)
    def describeContentRulesetCollection(self, id):
        return self._connection.get(url='/api/collections/{id}'.format(id=id))
    def modifyContentRulesetCollection(self, id, data):
        return self._connection.post(url='/api/collections/{id}'.format(id=id), payload=data)
    def deleteContentRulesetCollection(self, id):
        return self._connection.delete(url='/api/collections/{id}'.format(id=id))
    def listContentRuleset(self, id, limit=25,  query=None):
        params={'limit': limit}
        if query:
            params['query'] = query
        rtv = self._connection.get(url='/api/collections/{id}/rulesets'.format(id=id), params=params)
        items = rtv['rulesets']
        while "next" in rtv:
            params['cursor']= rtv['next']
            rtv = self._connection.get(url='/api/collections/{id}/rulesets'.format(id=id), params=params)
            items.extend(rtv['rulesets'])
        return items
    def createContentRuleset(self, id, payload):
        return self._connection.post(url='/api/collections/{id}/rulesets'.format(id=id), data=payload)
    def describeContentRuleset(self, id,rulesetID):
        return self._connection.get(url='/api/collections/{id}/rulesets/{rulesetID}'.format(id=id, rulesetID=rulesetID))
    def modifyContentRuleset(self, id, rulesetID, data):
        return self._connection.post(url='/api/collections/{id}/rulesets/{rulesetID}'.format(id=id, rulesetID=rulesetID), payload=data)
    def deleteContentRuleset(self, id,rulesetID):
        return self._connection.delete(url='/api/collections/{id}/rulesets/{rulesetID}'.format(id=id, rulesetID=rulesetID))




