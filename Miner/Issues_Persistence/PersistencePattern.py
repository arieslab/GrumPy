class PersistencePattern():
    def __init__(self, mode):
        self.mode = mode

    def issuePattern(self, issue_attributes):
        return {
            'Repository_Name' : issue_attributes[0],
            'Id' : issue_attributes[1],
            'Author' : issue_attributes[2],
            'Created_at' : issue_attributes[3],
            'Status' : issue_attributes[4],
            'Title' : issue_attributes[5],
            'Body' : issue_attributes[6],
            'Repository_Labels': issue_attributes[7],
            'Reactions': issue_attributes[8],
            'Events': issue_attributes[9],
            'Comments' : issue_attributes[10],
            'Issue_Labels' : issue_attributes[11],
            'Issue_Type': issue_attributes[12]
        }

    def eventPattern(self, event_attributes):
        return {
            'Issue': event_attributes[0],
            'Author': event_attributes[1],
            'Created_at': event_attributes[2],
            'Event': event_attributes[3],
            'Label': event_attributes[4]
        }

    def CommentsPattern(self, comments_attributes):
        return {
            'Author': comments_attributes[0],
            'Date': comments_attributes[1],
            'Comments': comments_attributes[2],
            'Reactions': comments_attributes[3],
        }
