import requests
import sys
from requests import exceptions
from github import Github, GithubException
from Miner.Activity_performance.RequestVerificationClass import VerificationClass
from Miner.Issues_Persistence.PersistencePattern import PersistencePattern


class MinerClass:
    def __init__(self, authentication, time_to_wait, set_num_requests, repo):
        self.repository = authentication.get_repo(str(repo))
        self.authentication = authentication
        self.time_to_wait = time_to_wait
        self.num_requests = set_num_requests

    def event_mining(self, issue):
        issue_events_list = []
        VerificationClass(self.authentication, self.time_to_wait, self.num_requests)

        try:
            VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
            for event in issue.get_events():
                VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                e = ''
                pattern = PersistencePattern()

                if (event.actor is None):
                    if (event.label is None):
                        event_formatted = pattern.eventPattern(issue.number, '-', event.created_at, event.event, '-')
                    else:
                        event_formatted = pattern.eventPattern(
                            issue.number, '-', event.created_at, event.event, event.label.name)

                else:
                    if (event.label is None):
                        event_formatted = pattern.eventPattern(
                            issue.number, event.actor.login, event.created_at, event.event, '-')
                    else:
                        event_formatted = pattern.eventPattern(
                            issue.number, event.actor.login, event.created_at, event.event, event.label.name)
                issue_events_list.append(event_formatted)
        except requests.exceptions.ReadTimeout as aes:
            print('ReadTimeout error in event mining')
            raise
        except requests.exceptions.ConnectionError as aes:
            print('Connection error in event mining')
            raise
        except GithubException as d:
            if (d.status == 403):
                print('Request limit achieved in event mining ')
                raise

        return issue_events_list

    def comments_mining(self, issue):
        issue_comments_list = []
        VerificationClass(self.authentication, self.time_to_wait, self.num_requests)

        try:
            for comment in issue.get_comments():
                VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                pattern = PersistencePattern()

                VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                reactions = self.reactions_mining(comment)

                if (comment.user is None):
                    comment_formatted = pattern.CommentsPattern('-', comment.created_at, comment.body, reactions)
                else:
                    comment_formatted = pattern.CommentsPattern(
                        comment.user.login, comment.created_at, comment.body, reactions)

                issue_comments_list.append(comment_formatted)

        except requests.exceptions.ReadTimeout as aes:
            print('ReadTimeout error in event mining')
            raise
        except requests.exceptions.ConnectionError as aes:
            print('Connection error in event mining')
            raise
        except GithubException as d:
            if (d.status == 403):
                print('Request limit achieved in event mining ')
                raise

        return issue_comments_list

    def reactions_mining(self, element):
        issue_reactions_list = []
        VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
        pattern = PersistencePattern()
        reactions_list = {'+1': 0,
                          'heart': 0,
                          'hooray': 0,
                          'confused': 0,
                          '-1': 0,
                          'laugh': 0,
                          'rocket': 0,
                          'eyes': 0}

        try:
            for reaction in element.get_reactions():
                VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                TheReaction = reaction.content

                reactions_list[str(TheReaction)] += 1

        except requests.exceptions.ReadTimeout as aes:
            print('ReadTimeout error in event mining')
            raise
        except requests.exceptions.ConnectionError as aes:
            print ('Connection error in event mining')
            raise
        except GithubException as d:
            if (d.status == 403):
                print('Request limit achieved in event mining ')
                raise

        return pattern.ReactionPattern(reactions_list)

    def repo_labels_mining(self):
        repo_labels_list = []
        VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
        pattern = PersistencePattern()

        try:
            for label in self.repository.get_labels():
                VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                repo_labels_list.append(label.name)
        except requests.exceptions.ReadTimeout as aes:
            print('ReadTimeout error in event mining')
            raise
        except requests.exceptions.ConnectionError as aes:
            print('Connection error in event mining')
            raise
        except GithubException as d:
            if (d.status == 403):
                print('Request limit achieved in event mining ')
                raise

        return pattern.LabelsPattern(repo_labels_list)

    def issue_labels_mining(self, issue):
        issue_labels_list = []
        VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
        pattern = PersistencePattern()

        try:
            for label in issue.get_labels():
                VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                issue_labels_list.append(label.name)
        except requests.exceptions.ReadTimeout as aes:
            print('ReadTimeout error in event mining')
            raise
        except requests.exceptions.ConnectionError as aes:
            print('Connection error in event mining')
            raise
        except GithubException as d:
            if (d.status == 403):
                print('Request limit achieved in event mining ')
                raise

        return pattern.LabelsPattern(issue_labels_list)


    def getLastIssue(self):
        VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
        try:
            for issue in self.repository.get_issues(state='all'):
                return int(issue.number)
        except GithubException as d:
            if (d.status == 404):
                print('Error 404')
                raise

    def getIssue(self, number):
        try:
            VerificationClass(self.authentication, self.time_to_wait, self.num_requests)
            issue = self.repository.get_issue(number)
            return issue
        except GithubException as f:
            if (f.status == 404):
                return None
        except AttributeError as a:
            return None

    def issue_mining(self, issue):
        pattern = PersistencePattern()

        issue_event = self.event_mining(issue)
        issue_comments = self.comments_mining(issue)
        issue_reactions = self.reactions_mining(issue)
        issue_labels = self.issue_labels_mining(issue)
        repository_labels = self.repo_labels_mining()
        VerificationClass(self.authentication, 1800, 5)
        return pattern.issuePattern(self.repository.name,
                                     issue.number,
                                     issue.user.login,
                                     issue.created_at,
                                     issue.state,
                                     issue.title,
                                     issue.body,
                                     repository_labels,
                                     issue_reactions,
                                     issue_event,
                                     issue_comments,
                                     issue_labels)
