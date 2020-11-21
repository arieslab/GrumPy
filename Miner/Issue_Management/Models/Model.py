from Miner.Issues_Persistence.Connections import Connections


class RepositoryClass:

    def __init__(self, name):
        self.repository_name = name
        self.amount_closed_issues = self.amount_open_issues = self.amount_of_issues = 0
        self.getAmountOfIssues('open')
        self.getAmountOfIssues('closed')
        self.getAmountOfIssues('all')
        self.repository_name_url = name.replace('/', '%2F')

    def getAmountOfIssues(self, state):
        db_Connection = Connections()

        db_Connection.openConnectionToDB()

        if (state == 'all'):
            self.amount_of_issues = db_Connection.getAmountInCollection(self.repository_name)
            return self.amount_of_issues
        elif (state == 'open'):
            self.amount_open_issues = db_Connection.getIssuesByStatus(self.repository_name, state).count()
            return self.amount_open_issues
        elif (state == 'closed'):
            self.amount_closed_issues = db_Connection.getIssuesByStatus(self.repository_name, state).count()
            return self.amount_closed_issues

        db_Connection.closeConnectionToDB()


class IssueIndex:
    def __init__(self, repoName, id, status, comments, reactions, events):
        self.id = id
        self.repository_name = repoName
        self.status = status
        self.comments = comments
        self.reactions = reactions
        self.events = events
        self.repository_name_url = repoName.replace('/', '%2F')

class Issue:
    def __init__(self, repo, id):
        self.repository = str(repo.replace('%2F', '/'))
        self.id = int(id)
        self.issueJson = self.getIssueInDB()

        self.createdAt = self.issueJson['Created_at']
        self.status = self.issueJson['Status']
        self.title = self.issueJson['Title']
        self.body = self.issueJson['Body']
        self.author = self.issueJson['Author']
        self.repository_labels = []
        self.issue_labels = []

        self.githubURL = 'http://www.github.com/'+str(self.repository)+'/issues/'+str(id)

        reactions = self.issueJson['Reactions']

        for label in self.issueJson['Repository_Labels']:
            self.repository_labels.append(label)

        for issueLabel in self.issueJson['Issue_Labels']:
            self.repository_labels.append(issueLabel)

        self.reactions = Reactions(reactions)

        self.issueEvent = []

        for event in self.issueJson['Events']:
            event_instance = Event(event)
            self.issueEvent.append(event_instance)

        self.issueComments = []
        comments = self.issueJson['Comments']

        if(comments != None):
            for comment in comments:
                comment = Comment(comment)
                self.issueComments.append(comment)

            self.amountComment = len(self.issueComments)


    def getIssueInDB(self):
        connection_instance = Connections()
        issue = connection_instance.findIssue(self.id, self.repository)
        connection_instance.closeConnectionToDB()

        return issue


class Reactions:
    def __init__(self, reactions):
        self.like       = reactions['Like']
        self.heart      = reactions['Heart']
        self.hooray     = reactions['Hooray']
        self.confused   = reactions['Confused']
        self.deslike    = reactions['Deslike']
        self.laught     = reactions['Laugh']
        self.rocket     = reactions['Rocket']
        self.eyes       = reactions['Eyes']

class Comment:
    def __init__(self, comment):
        self.author = comment['Author']
        self.created_at = comment['Date']
        self.text = comment['Comments']
        self.reactions = Reactions(comment['Reactions'])


class Event:
    def __init__(self, event):
        self.author = event['Author']
        self.created_at = event['Created_at']
        self.event = event['Event'].upper()
        self.label = event['Label']
