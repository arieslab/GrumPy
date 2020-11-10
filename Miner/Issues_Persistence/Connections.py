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
        self.client_db.close()

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
