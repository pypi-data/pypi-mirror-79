#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.
#import connect
#import config

class IdentityProviders:
    def __init__(self, config, connection):
        self._config=config
        self._connection = connection
    ##Users
    def listSAML(self, limit=25, expand="all", query=""):
        params={'limit': limit, 'expand':expand,'query':query}
        rtv = self._connection.get(url='/api/identity-providers/saml', params=params)
        items = rtv['providers']
        while "next" in rtv:
            params={'limit': limit, 'expand':expand,'query':query, 'cursor': rtv['next']}
            rtv = self._connection.get(url='/api/identity-providers/saml', params=params)
            items.extend(rtv['providers'])
        return items
    def createSAML(self, payload):
        return self._connection.post(url='/api/identity-providers/saml', data=payload)
    def describeSAML(self, id, expand="all"):
        params = {'expand': expand}
        return self._connection.get(url='/api/identity-providers/saml/{id}'.format(id=id), params=params )
    def modifySAML(self,id, payload):
        return self._connection.post(url='/api/identity-providers/saml/{id}'.format(id=id), data=payload)
    def deleteSAML(self, id):
        return self._connection.delete(url='/api/identity-providers/saml/{id}'.format(id=id))

