from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

def get_query(text):
    g = Graph()
    g.parse("linked_data.ttl", format="turtle")
    keywords = text.split()

    if keywords[0].lower() == "target":
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

        # target year
        target_year = " ".join(keywords[-1:])

        sparql_query = """
        PREFIX table: <http://www.semanticweb.org/fadil/ontologies/2023/7/ldt#/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?subject ?object
        WHERE {
            ?program rdfs:label ?programtitle .
            ?sasaran ?relation ?program .
            ?sasaran table:indikator ?temp .
            ?temp rdfs:label ?subject .
            ?temp table:target ?object
            FILTER (?programtitle = ?searchPattern)
        }
        """

        relation_uri = URIRef(f"table:{relation}")
        query = sparql_query.replace("?searchPattern", f"'{search_pattern}'").replace("?relation", f"{relation_uri}")
        results = g.query(query)
        for row in results:
            target = row['object'].value
            if target_year in target:
                indikator = row['subject'].value
                print(indikator, ", ", target)

    elif keywords[0].lower() == "apa":
        # relation
        if keywords[3][:2].lower() == "pn" or keywords[3].lower() == "prioritas" and keywords[4].lower() == "nasional":
            relation = "pn"
        elif keywords[2][:3].lower() == "rkp" or keywords[3].lower() == "rencana" and keywords[4].lower() == "kerja" and keywords[5].lower() == "pemerintah":
            relation = "penjabaran"

        # search pattern
        search_pattern = " ".join(keywords[3:])
        if "prioritas nasional" in search_pattern.lower():
            search_pattern = search_pattern.replace("prioritas nasional", "pn")
        if "rencana kerja pemerintah" in search_pattern.lower():
            search_pattern = search_pattern.replace("rencana kerja pemerintah", "rkp")

        # target year
        target_year = " ".join(keywords[-1:])

        sparql_query = """
        PREFIX table: <http://www.semanticweb.org/fadil/ontologies/2023/7/ldt#/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?subject ?object
        WHERE {
            ?subject ?relation ?object .
            FILTER (?object = ?searchPattern)
        }
        """

    relation_uri = URIRef(f"table:{relation}")
    query = sparql_query.replace("?searchPattern", f"'{search_pattern}'").replace("?relation", f"{relation_uri}")
    results = g.query(query)
 
    print(results)
    # for row in results:
    #     object = row['object'].value
    #     if target_year in object and object not in seen_targets:
    #         subject = row['subject'].value
    #         print(subject, ", ", object)
    #         seen_targets.add(object)