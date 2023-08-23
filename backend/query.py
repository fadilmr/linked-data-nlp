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
        extracted_data = []
        for row in results:
            target = row['object'].value
            if target_year in target:
                indikator = row['subject'].value
                extracted_data.append({"subject": indikator, "object": target})
        return extracted_data

    elif keywords[0].lower() == "apa":
        relation = ""
        # relation
        if keywords[2].lower() == "pn" or keywords[2].lower() == "prioritas" and keywords[3].lower() == "nasional":
            relation = "pndalam"
        elif keywords[3].lower() == "rkp" or keywords[3].lower() == "rencana" and keywords[4].lower() == "kerja" and keywords[5].lower() == "pemerintah":
            relation = "dijabarkan"
        elif keywords[2].lower() == "rpjmn" or keywords[2].lower() == "rencana" and keywords[3].lower() == "pembangunan" and keywords[4].lower() == "jangka" and keywords[5].lower() == "menengah" and keywords[6].lower() == "nasional":
            relation = "penjabaran"

        # search pattern
        if relation == "dijabarkan" or relation == "pndalam":
            search_pattern = " ".join(keywords[3:])
        else:
            search_pattern = " ".join(keywords[2:])

        if "prioritas nasional" in search_pattern.lower():
            search_pattern = search_pattern.replace("prioritas nasional", "pn")
        if "rencana kerja pemerintah" in search_pattern.lower():
            search_pattern = search_pattern.replace("rencana kerja pemerintah", "rkp")
        if "rencana pembangunan jangka menengah nasional" in search_pattern.lower():
            search_pattern = search_pattern.replace("rencana pembangunan jangka menengah nasional", "rpjmn")

        # target year
        target_year = " ".join(keywords[-1:])

        sparql_query = """
        PREFIX table: <http://www.semanticweb.org/fadil/ontologies/2023/7/ldt#/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?subject
        WHERE {
            ?program rdfs:label ?programtitle .
            ?temp ?relation ?program .
            ?temp table:deskripsi ?subject .
            FILTER (?programtitle = ?searchPattern)
        }
        """

        relation_uri = URIRef(f"table:{relation}")
        query = sparql_query.replace("?searchPattern", f"'{search_pattern}'").replace("?relation", f"{relation_uri}")
        results = g.query(query)
        extracted_data = []
        if relation == "pn":
            for row in results:
                subject = row['subject'].value
                if target_year in target:
                    extracted_data.append({"subject": subject,})
            return extracted_data
        else:
            for row in results:
                object = row['subject'].value
                extracted_data.append({"subject": object})
            return extracted_data

    
    # for row in results:
    #     object = row['object'].value
    #     if target_year in object and object not in seen_targets:
    #         subject = row['subject'].value
    #         print(subject, ", ", object)
    #         seen_targets.add(object)

def get_details(text):
    g = Graph()
    g.parse("linked_data.ttl", format="turtle")
    keywords = text

    sparql_query = """
        PREFIX table: <http://www.semanticweb.org/fadil/ontologies/2023/7/ldt#/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?individual ?predicate ?relatedIndividual
        WHERE {
            ?individual ?predicate ?relatedIndividual .
            FILTER (str(?individual) = ?individualUri)
        }
    """
    individual_uri = "http://www.semanticweb.org/fadil/ontologies/2023/7/ldt#/" + keywords
    query = sparql_query.replace("?individualUri", f"'{individual_uri}'")
    results = g.query(query)
    extracted_data = []
    for row in results:
        predicate = row['predicate']
        related_individual = row['relatedIndividual']
        extracted_data.append({"predicate": predicate, "relatedIndividual": related_individual})
    return extracted_data

    
def get_class():
    g = Graph()
    g.parse("linked_data.ttl", format="turtle")
    
    sparql_query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX table: <http://www.semanticweb.org/fadil/ontologies/2023/7/ldt#/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>    
        SELECT DISTINCT ?class ?label ?judul ?description
        WHERE {
            ?class a owl:Class.
            ?class rdfs:label ?label .
            ?class table:judul ?judul .
            ?class table:deskripsi ?description .
        }
    """

    results = g.query(sparql_query)
    extracted_data = []
    for row in results:
        class_name = row['class'].split("#")[1]
        label = row['label']
        judul = row['judul']
        deskripsi = row['description']
        extracted_data.append({"class": class_name, "label": label, "judul": judul, "deskripsi": deskripsi})
    return extracted_data