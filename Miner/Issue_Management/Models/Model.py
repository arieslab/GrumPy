from Miner.Issues_Persistence.Connections import Connections


class RepositoryClass:

    def __init__(self, name):
        self.repository_name = name
        self.amount_closed_issues = self.amount_open_issues = self.amount_of_issues = 0

    def getAmountOfIssues(self, state):
        db_Connection = Connections()

        db_Connection.openConnectionToDB()

        if(state == 'all'):
            self.amount_of_issues = db_Connection.getAmountInCollection(self.repository_name)
            return self.amount_of_issues
        elif(state == 'open'):
            self.amount_open_issues = db_Connection. getIssuesByStatus(self.repository_name, state).count()
            return self.amount_open_issues
        elif(state == 'closed'):
            self.amount_closed_issues = db_Connection.getIssuesByStatus(self.repository_name, state).count()
            return self.amount_closed_issues

        db_Connection.closeConnectionToDB()



