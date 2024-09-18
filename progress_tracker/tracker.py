from datetime import datetime


class ProgressTracker:
    def __init__(self):
        self.goals = {}  # user_id: list of goals
        self.activities = {}  # user_id: list of activities

    def set_goal(self, user_id, goal_description, target_date):
        if user_id not in self.goals:
            self.goals[user_id] = []
        self.goals[user_id].append({
            'description': goal_description,
            'target_date': target_date,
            'created_at': datetime.now(),
            'completed': False
        })
        return len(self.goals[user_id]) - 1  # Return the index of the new goal

    def complete_goal(self, user_id, goal_index):
        if user_id in self.goals and goal_index < len(self.goals[user_id]):
            self.goals[user_id][goal_index]['completed'] = True
            return True
        return False

    def get_goals(self, user_id):
        return self.goals.get(user_id, [])

    def log_activity(self, user_id, activity_type, details):
        if user_id not in self.activities:
            self.activities[user_id] = []
        self.activities[user_id].append({
            'type': activity_type,
            'details': details,
            'timestamp': datetime.now()
        })

    def get_activities(self, user_id, limit=10):
        return self.activities.get(user_id, [])[:limit]

    def get_progress_summary(self, user_id):
        goals = self.get_goals(user_id)
        activities = self.get_activities(user_id)
        completed_goals = sum(1 for goal in goals if goal['completed'])
        return {
            'total_goals': len(goals),
            'completed_goals': completed_goals,
            'recent_activities': len(activities)
        }
