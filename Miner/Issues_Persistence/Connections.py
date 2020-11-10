from pymongo import MongoClient

PLACE = 'localhost'
PORT = 27017
DB_NAME = 'GithubIssuesDB'

class Connections():
    def __init__(self):
        self.client, self.issues_db = self.openConnectionToDB()

    def openConnectionToDB(self):
        mongodb_client = MongoClient(PLACE,
                                     PORT)

        issues_database = mongodb_client[DB_NAME]

        return mongodb_client, issues_database

    def closeConnectionToDB(self):
        self.client_db.close()

