import logging
import rdflib

# configuring logging
logging.basicConfig()

# creating the graph
g=rdflib.Graph()
result=g.parse("result_bonus.owl", "xml")
print("graph has %s statements.\n" % len(g))

# Query to return 10 movies filmed in countries with population > 100 million: FILTER (?population > 10000000)
# FILTER regex(str(?countryName_movie), str(?countryName_country)) line is a neat trick to combine movies 
# and countries information. For example population information is from factbook (not all info is in DBpedia, 
# and definitely not in the format needed for my ontology), whereas movies info is from DBpedia (not in factbook).
query1="""
PREFIX mc: <http://www.semanticweb.org/zhanelya/ontologies/2015/2/untitled-ontology-19#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?population
WHERE { ?film rdf:type mc:Movie .
        ?film mc:movieName ?movieName .
        ?film mc:filmedIn ?countryName_movie .
		?country rdf:type mc:Country .
        ?country mc:countryName ?countryName_country .
        ?country mc:population ?population .
		FILTER regex(str(?countryName_movie), str(?countryName_country))
		FILTER (?population > 100000000)
        }LIMIT 10
        """

# querying and displaying the results
print ('{0:40s} {1:20s} {2:10s}'.format("Title","Filmed in","Population"))
print ('{0:40s} {1:20s} {2:10s}'.format("----------------------------------------","--------------------","------------------"))
for x,y,z in g.query(query1):
    print ('{0:40s} {1:20s} {2:10s}'.format(x.encode('utf-8'),y.encode('utf-8'),z))
	#converted to utf, as other formats cannot be displayed in Windows terminal
    
print "\n\n"

# Query	to return movies filmed in countries that has a capital "Buenos Aires"
query2="""
PREFIX mc: <http://www.semanticweb.org/zhanelya/ontologies/2015/2/untitled-ontology-19#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?capital
WHERE { ?film rdf:type mc:Movie .
        ?film mc:movieName ?movieName .
        ?film mc:filmedIn ?countryName_movie .
		?country rdf:type mc:Country .
        ?country mc:countryName ?countryName_country .
        ?country mc:capital ?capital .
		FILTER regex(str(?countryName_movie), str(?countryName_country))
		FILTER regex(str(?capital),"Buenos Aires")
        }
        """
		
# querying and displaying the results
print ('{0:40s} {1:20s} {2:10s}'.format("Title","Filmed in","Capital"))
print ('{0:40s} {1:20s} {2:10s}'.format("----------------------------------------","--------------------","------------------"))
for x,y,z in g.query(query2):
    print ('{0:40s} {1:20s} {2:10s}'.format(x.encode('utf-8'),y.encode('utf-8'),z.encode('utf-8')))
	#converted to utf, as other formats cannot be displayed in Windows terminal

print "\n\n"

# Query	to return movies filmed in countries that have birthrate between 10 and 20	
query3="""
PREFIX mc: <http://www.semanticweb.org/zhanelya/ontologies/2015/2/untitled-ontology-19#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?birthrate
WHERE { ?film rdf:type mc:Movie .
        ?film mc:movieName ?movieName .
        ?film mc:filmedIn ?countryName_movie .
		?country rdf:type mc:Country .
        ?country mc:countryName ?countryName_country .
        ?country mc:birthrate ?birthrate .
		FILTER regex(str(?countryName_movie), str(?countryName_country))
		FILTER (?birthrate > 15.00 && ?birthrate < 20.00)
        }
        """
# querying and displaying the results
print ('{0:40s} {1:20s} {2:10s}'.format("Title","Filmed in","Birthrate"))
print ('{0:40s} {1:20s} {2:10s}'.format("----------------------------------------","--------------------","------------------"))
for x,y,z in g.query(query3):
    print ('{0:40s} {1:20s} {2:10s}'.format(x.encode('utf-8'),y.encode('utf-8'),z))
	#converted to utf, as other formats cannot be displayed in Windows terminal

print "\n\n"
	
# Query	to return movies filmed in countries having common land boundary with Kazakhstan
query4="""
PREFIX mc: <http://www.semanticweb.org/zhanelya/ontologies/2015/2/untitled-ontology-19#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
SELECT DISTINCT ?movieName ?countryName_country ?landboundary
WHERE { ?film rdf:type mc:Movie .
        ?film mc:movieName ?movieName .
        ?film mc:filmedIn ?countryName_movie .
		?country rdf:type mc:Country .
        ?country mc:countryName ?countryName_country .
        ?country mc:landboundary ?landboundary .
		FILTER regex(str(?countryName_movie), str(?countryName_country))
		FILTER regex(str(?landboundary),"Kazakhstan")
        }
        """
# querying and displaying the results
print ('{0:30s} {1:10s} {2:10s}'.format("Title","Filmed in","Neighbouring country"))
print ('{0:30s} {1:10s} {2:10s}'.format("------------------------------","---------","--------------------"))
for x,y,z in g.query(query4):
    print ('{0:30s} {1:10s} {2:10s}'.format(x.encode('utf-8'),y.encode('utf-8'),z.encode('utf-8')))
	#converted to utf, as other formats cannot be displayed in Windows terminal