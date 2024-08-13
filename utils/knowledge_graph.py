import json
import networkx as nx

class KnowledgeGraph:
    def __init__(self, graph_file):
        with open(graph_file, 'r') as f:
            graph_data = json.load(f)
        self.graph = nx.node_link_graph(graph_data)

    def get_related_concepts(self, concept, depth=2):
        related = set()
        for node in nx.dfs_preorder_nodes(self.graph, source=concept, depth_limit=depth):
            related.add(node)
        return list(related)

    def get_prerequisites(self, concept):
        return list(self.graph.predecessors(concept))

    def get_next_topics(self, concept):
        return list(self.graph.successors(concept))