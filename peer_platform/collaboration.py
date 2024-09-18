from datetime import datetime


class PeerCollaborationPlatform:
    def __init__(self):
        self.discussions = {}  # book_id: list of discussion posts
        self.study_groups = {}  # group_id: {name, members, book_ids}

    def add_discussion_post(self, book_id, user_id, content):
        if book_id not in self.discussions:
            self.discussions[book_id] = []
        post = {
            'user_id': user_id,
            'content': content,
            'timestamp': datetime.now(),
            'replies': []
        }
        self.discussions[book_id].append(post)
        return post

    def get_discussion_posts(self, book_id):
        return self.discussions.get(book_id, [])

    def add_reply(self, book_id, post_index, user_id, content):
        if book_id in self.discussions and post_index < len(self.discussions[book_id]):
            reply = {
                'user_id': user_id,
                'content': content,
                'timestamp': datetime.now()
            }
            self.discussions[book_id][post_index]['replies'].append(reply)
            return reply
        return None

    def create_study_group(self, name, creator_id, book_ids):
        group_id = len(self.study_groups) + 1
        self.study_groups[group_id] = {
            'name': name,
            'members': [creator_id],
            'book_ids': book_ids
        }
        return group_id

    def join_study_group(self, group_id, user_id):
        if group_id in self.study_groups:
            self.study_groups[group_id]['members'].append(user_id)
            return True
        return False

    def get_study_group(self, group_id):
        return self.study_groups.get(group_id)

    def get_user_study_groups(self, user_id):
        return [group for group in self.study_groups.values() if user_id in group['members']]
