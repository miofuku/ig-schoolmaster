from datetime import datetime
from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate


class KnowledgeMapper:
    def __init__(self):
        self.maps = {}  # user_id: list of maps
        self.llm = OpenAI(temperature=0.7)

    def create_map(self, user_id, title):
        if user_id not in self.maps:
            self.maps[user_id] = []
        new_map = {
            'id': len(self.maps[user_id]) + 1,
            'title': title,
            'nodes': [],
            'edges': [],
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        self.maps[user_id].append(new_map)
        return new_map['id']

    def generate_insight(self, topic):
        template = PromptTemplate(
            input_variables=["topic"],
            template="What are the key concepts and connections related to {topic}?"
        )
        chain = LLMChain(llm=self.llm, prompt=template)
        return chain.run(topic=topic)

    def add_node(self, user_id, map_id, label, x, y):
        map_data = self.get_map(user_id, map_id)
        if map_data:
            node_id = len(map_data['nodes']) + 1
            map_data['nodes'].append({
                'id': node_id,
                'label': label,
                'x': x,
                'y': y
            })
            map_data['updated_at'] = datetime.now()
            return node_id
        return None

    def add_edge(self, user_id, map_id, source_id, target_id, label=''):
        map_data = self.get_map(user_id, map_id)
        if map_data:
            edge_id = len(map_data['edges']) + 1
            map_data['edges'].append({
                'id': edge_id,
                'source': source_id,
                'target': target_id,
                'label': label
            })
            map_data['updated_at'] = datetime.now()
            return edge_id
        return None

    def get_map(self, user_id, map_id):
        if user_id in self.maps:
            return next((m for m in self.maps[user_id] if m['id'] == map_id), None)
        return None

    def get_user_maps(self, user_id):
        return self.maps.get(user_id, [])

    def update_node(self, user_id, map_id, node_id, label=None, x=None, y=None):
        map_data = self.get_map(user_id, map_id)
        if map_data:
            node = next((n for n in map_data['nodes'] if n['id'] == node_id), None)
            if node:
                if label is not None:
                    node['label'] = label
                if x is not None:
                    node['x'] = x
                if y is not None:
                    node['y'] = y
                map_data['updated_at'] = datetime.now()
                return True
        return False

    def update_edge(self, user_id, map_id, edge_id, label=None):
        map_data = self.get_map(user_id, map_id)
        if map_data:
            edge = next((e for e in map_data['edges'] if e['id'] == edge_id), None)
            if edge and label is not None:
                edge['label'] = label
                map_data['updated_at'] = datetime.now()
                return True
        return False

    def delete_node(self, user_id, map_id, node_id):
        map_data = self.get_map(user_id, map_id)
        if map_data:
            map_data['nodes'] = [n for n in map_data['nodes'] if n['id'] != node_id]
            map_data['edges'] = [e for e in map_data['edges'] if e['source'] != node_id and e['target'] != node_id]
            map_data['updated_at'] = datetime.now()
            return True
        return False

    def delete_edge(self, user_id, map_id, edge_id):
        map_data = self.get_map(user_id, map_id)
        if map_data:
            map_data['edges'] = [e for e in map_data['edges'] if e['id'] != edge_id]
            map_data['updated_at'] = datetime.now()
            return True
        return False

# Example usage:
# mapper = KnowledgeMapper()
# map_id = mapper.create_map('user1', 'My Literature Concepts')
# node1 = mapper.add_node('user1', map_id, 'Character Development', 100, 100)
# node2 = mapper.add_node('user1', map_id, 'Plot Structure', 200, 200)
# edge = mapper.add_edge('user1', map_id, node1, node2, 'Influences')
