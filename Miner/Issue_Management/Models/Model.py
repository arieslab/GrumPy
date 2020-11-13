from Miner.Issues_Persistence.Connections import Connections


class RepositoryClass:

    def __init__(self, name):
        self.repository_name = name
        self.amount_closed_issues = self.amount_open_issues = self.amount_of_issues = 0

    def getAmountOfIssues(self):
        db_Connection = Connections()

        db_Connection.openConnectionToDB()

        repository = db_Connection[self.repository_name]

        self.amount_of_issues = repository.count()

        print(self.amount_of_issues)

        db_Connection.closeConnectionToDB()


