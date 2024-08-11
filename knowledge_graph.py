import networkx as nx
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDFS, OWL

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.rdf_graph = Graph()

    def load_from_rdf(self, rdf_file):
        self.rdf_graph.parse(rdf_file, format="turtle")
        for s, p, o in self.rdf_graph:
            self.graph.add_edge(str(s), str(o), relation=str(p))

    def get_related_concepts(self, concept, depth=2):
        if concept not in self.graph:
            return []
        related = nx.dfs_predecessors(self.graph, concept, depth)
        return list(related.keys()) + list(set([item for sublist in related.values() for item in sublist]))

    def verify_statement(self, subject, predicate, object):
        subject = URIRef(subject)
        object = URIRef(object)
        return (subject, predicate, object) in self.rdf_graph