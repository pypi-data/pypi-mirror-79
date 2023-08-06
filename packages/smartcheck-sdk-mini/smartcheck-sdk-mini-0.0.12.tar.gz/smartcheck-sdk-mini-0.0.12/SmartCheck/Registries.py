#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class Registries:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    def list(self, limit=25, expand="all", query=None):
        params={'limit': limit, 'expand':expand}
        if query:
            params['query'] = query
        rtv = self._connection.get(url='/api/registries', params=params)
        items = rtv['registries']
        while "next" in rtv:
            params['cursor'] = rtv['next']
            rtv = self._connection.get(url='/api/registries', params=params)
            items.extend(rtv['registries'])
        return items
    def create(self, payload):
        return self._connection.post(url='/api/registries', data=payload)
    def describe(self, id):
        return self._connection.get(url='/api/registries/{id}'.format(id=id))
    def modify(self, id, data):
        return self._connection.post(url='/api/registries/{id}'.format(id=id), payload=data)
    def delete(self, id):
        return self._connection.delete(url='/api/registries/{id}'.format(id=id))
    def listRegistryImages(self, id):
        return self._connection.get(url='/api/registries/{id}/images'.format(id=id))
    def describeRegistryImage(self, id, imageID):
        return self._connection.get(url='/api/registries/{id}/images/{imageID}'.format(id=id, imageID=imageID))
    def describeRegistryDashboard(self):
        return self._connection.get(url='/api/registries/dashboard')
    def createRegistryScan(self, id, payload):
        return self._connection.post(url='/api/registries/{id}/scans'.format(id=id), data=payload)
