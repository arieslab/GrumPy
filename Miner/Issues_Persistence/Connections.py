from pymongo import MongoClient

PLACE = 'localhost'
PORT = 27017
DB_NAME = 'GithubIssuesDB'


class Connections:
    def __init__(self):
        self.client, self.issues_db = self.openConnectionToDB()

    def openConnectionToDB(self):
        mongodb_client = MongoClient(PLACE,
                                     PORT)

        issues_database = mongodb_client[DB_NAME]

        return mongodb_client, issues_database

    def closeConnectionToDB(self):
        self.client.close()

    def saveJsonAsIssue(self, json_data, collection_name):
        self.issues_db[str(collection_name)].insert(json_data)

    def deleteIssue(self, number, collection_name):
        self.issues_db[str(collection_name)].delete_one({'Id': number})

    def verifyMiningFinishing(self, first_issue, collection_name):
        if (self.issues_db[str(collection_name)].find_one({'Id': first_issue})):
            return True

        return False

    def verifyCollectionInDatabase(self, collection_name):
        if (collection_name in self.issues_db.list_collection_names()):
            return True

        return False

    def verifyLastIssueInCollection(self, collection_name):
        repo_colletion = self.issues_db[collection_name]
        issue = 0

        for i in repo_colletion.find({}):
            issue = i

        return issue['Id']

    def findIssue(self, number, repo):
        return self.issues_db[repo].find_one({'Id': number})

    def getAmountInCollection(self, name_collection):
        return self.issues_db[name_collection].count()

    def getIssuesByStatus(self, name_collection, status):
        return self.issues_db[name_collection].find({'Status': status})

    def getAmountOfIssuesInDBByStatus(self, status):
        list_of_col = self.issues_db.list_collection_names()
        amount_of_issues = 0

        for collection in list_of_col:
            amount_of_issues += self.issues_db[collection].find({'Status': status}).count()

        return amount_of_issues




