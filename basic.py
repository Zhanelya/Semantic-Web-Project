import logging
import rdflib
from rdflib.graph import Graph, URIRef
from SPARQLWrapper import SPARQLWrapper, RDF
from rdflib.plugins.memory import IOMemory

# configuring logging
logging.basicConfig()
 
# configuring the end-point and constructing query
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
construct_query="""
      PREFIX movie: <http://www.semanticweb.org/zhanelya/ontologies/2015/2/untitled-ontology-19#>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>        
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
      PREFIX dbpprop: <http://dbpedia.org/property/>
      
      CONSTRUCT {
      ?film rdf:type movie:Movie .
      ?film movie:movieName ?name .
	  ?film movie:budget ?budget .
	  ?film movie:movieDescription ?abstract .
	  ?film movie:durationSeconds ?runtime . 
	  ?film movie:movieLanguageOf ?language .
	  ?language rdf:type movie:Language .
	  ?film movie:hasActor ?actor .
      ?actor rdf:type movie:Actor .
	  ?film movie:hasMusicBy ?musicComposer .
      ?musicComposer rdf:type movie:Composer .
	  ?film movie:directedBy ?director .
      ?director rdf:type movie:Director .
      ?film movie:producedBy ?producer .
      ?producer rdf:type movie:Producer .
	  ?film movie:cinematographyBy ?cinematography .
      ?cinematography rdf:type movie:Cinematographer .
	  ?film movie:distributedBy ?distributor .
      ?distributor rdf:type movie:Distributor .
	  ?film movie:filmedIn ?country .
	  ?country rdf:type movie:Country .
      ?film movie:writtenBy ?screenwriter .
      ?screenwriter rdf:type movie:Screenwriter .
      }
       WHERE{
       ?film rdf:type dbpedia-owl:Film .
       ?film foaf:name ?name .
	   OPTIONAL {?film dbpprop:budget ?budget}
	   OPTIONAL {?film dbpedia-owl:abstract ?abstract} 
       OPTIONAL {?film dbpprop:runtime ?runtime}
	   OPTIONAL {?film dbpedia-owl:language ?language}
       OPTIONAL {?film dbpedia-owl:starring ?actor} 
       OPTIONAL {?film dbpedia-owl:musicComposer ?musicComposer} 
	   OPTIONAL {?film dbpedia-owl:director ?director}
       OPTIONAL {?film dbpedia-owl:producer ?producer}
       OPTIONAL {?film dbpedia-owl:cinematography ?cinematography}
       OPTIONAL {?film dbpedia-owl:distributor ?distributor}
       OPTIONAL {?film dbpedia-owl:country ?country}
       OPTIONAL {?film dbpedia-owl:writer ?screenwriter}
	   FILTER (LANG(?name)="en")
	   FILTER (LANG(?abstract)="en")
	   }
	   LIMIT 100000
	   """
sparql.setQuery(construct_query)
sparql.setReturnFormat(RDF)

# creating the RDF store and graph
memory_store=IOMemory()
graph_id=URIRef("http://www.semanticweb.org/store/movie")
g = Graph(store=memory_store, identifier=graph_id)
rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

# merging results and saving the store
g = sparql.query().convert()
g.parse("ontology.owl")
g.serialize("result_basic.owl", "xml")
