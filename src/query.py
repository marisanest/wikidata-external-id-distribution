from endpoint import SPARQLEndpoint
from exceptions import TypeError


class Query(object):

    def __init__(self, query):
        self.endpoint = SPARQLEndpoint()
        self.query = query
        self.result = None

    def execute(self):
        self.result = self.endpoint.execute(self.query)
        return self

    def extract(self):
        raise NotImplementedError


class ExternalIdsQuery(Query):

    QUERY = '''
                SELECT ?property ?propertyLabel
                WHERE {
                    ?property wikibase:propertyType wikibase:ExternalId .
  
                    SERVICE wikibase:label {
                        bd:serviceParam wikibase:language "de, en" .
                    }          
                }
            '''

    def __init__(self):
        super().__init__(ExternalIdsQuery.QUERY)

    def extract(self):
        print(self.result)
        if self.result is None:
            raise TypeError('result')
        return [
            {
                'property': binding['property']['value'],
                'propertyLabel': binding['propertyLabel']['value']
            } for binding in self.result['results']['bindings']
        ]


class ExternalIdCountQuery(Query):

    QUERY = '''
                SELECT (COUNT(?propertyclaim) AS ?count) 
                WHERE {
                    <##> wikibase:claim ?propertyclaim .
                    [] ?propertyclaim [] .
                }
            '''

    def __init__(self, id):
        super().__init__(ExternalIdCountQuery.QUERY.replace('##', id))

    def extract(self):
        if self.result is None:
            raise TypeError('result')
        return int([binding['count']['value'] for binding in self.result['results']['bindings']][0])
