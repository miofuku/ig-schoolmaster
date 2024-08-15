import json
import networkx as nx
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class KnowledgeGraph:
    def __init__(self, graph_file):
        with open(graph_file, 'r') as f:
            self.graph_data = json.load(f)
        self.G = nx.node_link_graph(self.graph_data)
        self.stop_words = set(stopwords.words('english'))

    def query(self, input_text):
        tokens = word_tokenize(input_text.lower())
        tokens = [t for t in tokens if t not in self.stop_words]
        
        relevant_nodes = []
        for token in tokens:
            if token in self.G.nodes:
                relevant_nodes.append(token)
                relevant_nodes.extend(list(self.G.neighbors(token)))
        
        return ' '.join(set(relevant_nodes))

    def extract_topics(self, text):
        tokens = word_tokenize(text.lower())
        return [t for t in tokens if t in self.G.nodes]

    def extract_interests(self, text):
        tokens = word_tokenize(text.lower())
        return [t for t in tokens if t in self.G.nodes and self.G.nodes[t].get('type') == 'interest']