from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

def get_query(text):
    keywords = text.split()

    # relation
    relation = ""
    if keywords[2][:2].lower() == "pn" or keywords[2].lower() == "prioritas" and keywords[3].lower() == "nasional":
        relation = "ssrnpn"
    elif keywords[2][:2].lower() == "pp" or keywords[2].lower() == "program" and keywords[3].lower() == "prioritas":
        relation = "ssrnpp"
        
    # search pattern
    search_pattern = " ".join(keywords[2:])
    if "prioritas nasional" in search_pattern.lower():
        search_pattern = search_pattern.replace("prioritas nasional", "pn")
    if "program prioritas" in search_pattern.lower():
        search_pattern = search_pattern.replace("program prioritas", "pp")

    sparql_query = """
    PREFIX table: <http://www.semanticweb.org/fadil/ontologies/2023/7/ldt#/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?indikator ?target
    WHERE {
        ?program rdfs:label ?programtitle .
        ?sasaran ?relation ?program .
        ?sasaran table:indikator ?temp .
        ?temp rdfs:label ?indikator .
        ?temp table:target ?target
        FILTER (?programtitle = ?searchPattern)
    }
    """

    relation_uri = URIRef(f"table:{relation}")
    query = sparql_query.replace("?searchPattern", f"'{search_pattern}'").replace("?relation", f"{relation_uri}")

    return query

def get_result(query):
    g = Graph()
    g.parse("linked_data.ttl", format="turtle")
    
    results = g.query(query)

    for row in results:
        indikator = row['indikator'].value
        target = row['target'].value
        print(indikator,', ', target)