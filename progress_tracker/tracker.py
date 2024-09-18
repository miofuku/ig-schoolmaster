class ProgressTracker:
    def __init__(self):
        self.goals = {}

    def update_progress(self, goal):
        if goal not in self.goals:
            self.goals[goal] = 0
        self.goals[goal] += 1
        return self.goals[goal]