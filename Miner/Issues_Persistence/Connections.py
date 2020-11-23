from pymongo import MongoClient
import collections

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

    def getAmountOfCommentsByStatus(self, name_collection, status):
        issues = self.issues_db[name_collection].find({'Status': status})
        comment_counter = 0


        for issue in issues:
            if(issue['Comments'] != None):
                comment_counter += len(list(issue['Comments']))

        return comment_counter

    def getAmountOfReactions(self, name_colletion):
        issues = self.issues_db[name_colletion].find({})
        reactions = {
            'Like':  0, 'Heart':   0, 'Hooray':   0, 'Confused':   0, 'Deslike':   0, 'Laugh':   0, 'Rocket':   0, 'Eyes':   0
        }

        for issue in issues:
            issue_reactions = issue['Reactions']

            for i in issue_reactions:
                reactions[i] += issue_reactions[i]

            try:
                if (issue['Comments'] == None):
                    return reactions
            except TypeError:
                    return reactions

            for comment in issue['Comments']:
                comment_reactions = comment['Reactions']

                for c in comment_reactions:
                    reactions[c] += comment_reactions[c]

        return reactions

    def getAmountOfEvents(self, name_collection):
        issues = self.issues_db[name_collection].find({})
        event_list = []

        for issue in issues:
            issue_event = issue['Events']

            for e in issue_event:
                event_list.append(e['Event'])

        count_events = collections.Counter(event_list)

        top10_events = count_events.most_common(10)

        return top10_events

    def getIssuesByStatus(self, name_collection, status):
        return self.issues_db[name_collection].find({'Status': status})

    def getAmountOfIssuesInDBByStatus(self, status):
        list_of_col = self.issues_db.list_collection_names()
        amount_of_issues = 0

        for collection in list_of_col:
            amount_of_issues += self.issues_db[collection].find({'Status': status}).count()

        return amount_of_issues

    def getAmountOfRepos(self):
        list_of_col = len(self.issues_db.list_collection_names())

        return list_of_col

    def getListOfRepo(self):
        return self.issues_db.list_collection_names()

    def getListOfIssues(self, name_collection):
        return self.issues_db[name_collection].find({})


