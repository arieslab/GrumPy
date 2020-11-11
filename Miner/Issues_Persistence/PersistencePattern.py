class PersistencePattern:
    def __init__(self):
        pass

    def issuePattern(self, repo_name, id, author, created_date, status, title, body, repo_labels, reactions, events,
                     comments, issue_labels):
        return {
            'Repository_Name': repo_name,
            'Id': id,
            'Author': author,
            'Created_at': created_date,
            'Status': status,
            'Title': title,
            'Body': body,
            'Repository_Labels': repo_labels,
            'Reactions': reactions,
            'Events': events,
            'Comments': comments,
            'Issue_Labels': issue_labels
        }

    def eventPattern(self, issue, author, created_at, event, label):
        return {
            'Issue': issue,
            'Author': author,
            'Created_at': created_at,
            'Event': event,
            'Label': label
        }

    def CommentsPattern(self, author, date, comments, reactions):
        return {
            'Author': author,
            'Date': date,
            'Comments': comments,
            'Reactions': reactions
        }

    def LabelsPattern(self, labels_attributes):
        return {
            'name': labels_attributes
        }

    def ReactionPattern(self, reaction_list):
        return {
            'Like'      :   reaction_list['+1'],
            'Heart'     :   reaction_list['heart'],
            'Hooray'    :   reaction_list['hooray'],
            'Confused'  :   reaction_list['confused'],
            'Deslike'   :   reaction_list['-1'],
            'Laugh'     :   reaction_list['laugh'],
            'Rocket'    :   reaction_list['rocket'],
            'Eyes'      :   reaction_list['eyes']
        }
