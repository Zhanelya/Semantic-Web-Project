import logging
import rdflib
from rdflib import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory


# configuring logging
logging.basicConfig()

# configuring the end-point and constructing query
sparql = SPARQLWrapper("http://wifo5-04.informatik.uni-mannheim.de/factbook/sparql")
construct_query="""

      PREFIX mc: <http://www.semanticweb.org/zhanelya/ontologies/2015/2/untitled-ontology-19#>
	  PREFIX db: <http://wifo5-04.informatik.uni-mannheim.de/factbook/resource/>
	  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	  PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	  PREFIX d2r: <http://sites.wiwiss.fu-berlin.de/suhl/bizer/d2r-server/config.rdf#>
	  PREFIX owl: <http://www.w3.org/2002/07/owl#>
	  PREFIX map: <file:/var/www/wbsg.de/factbook/factbook.n3#>
	  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
	  PREFIX factbook: <http://wifo5-04.informatik.uni-mannheim.de/factbook/ns#>
	  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

	  
      CONSTRUCT {
      ?country rdf:type mc:Country .
      ?country mc:countryName ?name .
	  ?country mc:capital ?capital_name .
	  ?country mc:areaTotal ?area_total .
	  ?country mc:areaLand ?area_land .
	  ?country mc:areaWater ?area_water .
	  ?country mc:countryDescription ?background .
	  ?country mc:timeZone ?capital_timedifference .
	  ?country mc:currency ?currency .
	  ?country mc:climate ?climate .
	  ?country mc:birthrate ?birthrate .
	  ?country mc:deathrate ?deathrate .
	  ?country mc:population ?population .
	  ?country mc:landboundary ?landboundary .
	  ?landboundary rdf:type mc:Country .
	  }
       WHERE{
       ?country rdf:type factbook:Country .
       ?country factbook:name ?name .
       ?country factbook:capital_name ?capital_name .
	   ?country factbook:area_total ?area_total .
	   ?country factbook:area_land ?area_land .
	   ?country factbook:area_water ?area_water .
	   ?country factbook:background ?background .
	   ?country factbook:capital_timedifference ?capital_timedifference .
	   ?country factbook:currency_code ?currency .
	   ?country factbook:climate ?climate .
	   ?country factbook:birthrate ?birthrate .
	   ?country factbook:deathrate ?deathrate .
	   ?country factbook:population_total ?population .
	   ?country factbook:landboundary ?landboundary .
	   
       }"""

sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graph_id=URIRef('http://www.semanticweb.org/store/movie_country')
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store 
g = sparql.query().convert()
g.parse("result_basic.owl")
# the graph will be saved as full_example.owl. You can open the file with Protege to inspect it.
g.serialize("result_bonus.owl", "xml")
