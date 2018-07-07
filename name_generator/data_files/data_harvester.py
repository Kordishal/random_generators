import json
from rdflib import Graph, OWL, RDF, RDFS, URIRef, Literal, Namespace
import csv
import re
from random_names import NameSet

def lake_dbpadia(file_name):

    with open(file_name, 'r') as file:
        content = json.loads(file.read())

        DBPEDIA = Namespace('http://dbpedia.org/ontology/')
        DBPEDIARESOURCE = Namespace('http://dbpedia.org/resource/')

        g = Graph()
        g.bind('owl', OWL)
        g.bind('dbo', DBPEDIA)
        g.bind('dbr', DBPEDIARESOURCE)
        g.bind('georss', Namespace('http://www.georss.org/georss/'))
        g.bind('geo', Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#'))
        g.bind('wikidata', Namespace('http://www.wikidata.org/entity/'))
        g.bind('schema', Namespace('http://schema.org/'))

        for properties in content['properties']:
            subject = URIRef(properties['propertyURI'])
            g.add((subject, RDF.type, RDF.Property))

            label = Literal(properties['propertyLabel'], lang='en')
            g.add((subject, RDFS.label, label))

            pro_type = URIRef(properties['propertyType'])
            g.add((subject, RDFS.range, pro_type))

        for instances in content['instances']:
            print(instances)
            key = [key for key in instances][0]
            subject = URIRef(key)
            g.add((subject, RDF.type, DBPEDIA.Lake))

            for item in instances[key]:
                print(item)
                obj = instances[key][item]
                if not obj == 'NULL':
                    if isinstance(obj, list):
                        for el in obj:
                            print(el)
                            if el.startswith('http://'):
                                g.add((subject, URIRef(item), URIRef(el)))
                            else:
                                g.add((subject, URIRef(item), Literal(el, lang='en')))
                    else:
                        print(obj)
                        if obj.startswith('http://'):
                            g.add((subject, URIRef(item), URIRef(obj)))
                        else:
                            g.add((subject, URIRef(item), Literal(obj, lang='en')))

        g.serialize('lakes.ttl', format='ttl')


if __name__ == '__main__':
    lake_dbpadia('Lake.json')



