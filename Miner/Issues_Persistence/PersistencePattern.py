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
