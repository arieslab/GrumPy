import requests
import sys
from requests import exceptions
from github import Github, GithubException
from Miner.Activity_performance import RequestVerificationClass
from Miner.Issues_Persistence.PersistencePattern import PersistencePattern


class MinersClass:
    def __init__(self, issue, authentication, time_to_wait, set_num_requests, repository):
        self.issue = issue
        self.repository = repository
        self.authentication = authentication
        self.time_to_wait = time_to_wait
        self.num_requests = set_num_requests

    def event_mining(self, issue):
        issue_events_list = []
        RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)

        try:

            for event in self.issue.get_events():
                RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                e = ''
                pattern = PersistencePattern()

                if (event.actor is None):
                    if (event.label is None):
                        event_formatted = pattern.eventPattern([issue.number, '-', event.created_at, event.event, '-'])
                    else:
                        event_formatted = pattern.eventPattern(
                            [issue.number, '-', event.created_at, event.event, event.label.name])

                else:
                    if (event.label is None):
                        event_formatted = pattern.eventPattern(
                            [issue.number, event.actor.login, event.created_at, event.event, '-'])
                    else:
                        event_formatted = pattern.eventPattern(
                            [issue.number, event.actor.login, event.created_at, event.event, event.label.name])
                issue_events_list.append(event_formatted)
        except requests.exceptions.ReadTimeout as aes:
            raise SystemError('ReadTimeout error in event mining')
        except requests.exceptions.ConnectionError as aes:
            raise SystemError('Connection error in event mining')
        except GithubException as d:
            if (d.status == 403):
                raise SystemError('Request limit achieved in event mining ')

        return issue_events_list

    def comments_mining(self):
        issue_comments_list = []
        RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)

        try:
            for comment in self.issue.get_comments():
                RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                pattern = PersistencePattern()

                RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                reactions = self.reactions_mining(comment)

                if (comment.user is None):
                    comment_formatted = pattern.CommentsPattern(['-', comment.created_at, comment.body, reactions])
                else:
                    comment_formatted = pattern.CommentsPattern(
                        [comment.user.login, comment.created_at, comment.body, reactions])

                issue_comments_list.append(comment_formatted)


        except requests.exceptions.ReadTimeout as aes:
            raise SystemError('ReadTimeout error in event mining')
        except requests.exceptions.ConnectionError as aes:
            raise SystemError('Connection error in event mining')
        except GithubException as d:
            if (d.status == 403):
                raise SystemError('Request limit achieved in event mining ')

    def reactions_mining(self, element):
        issue_reactions_list = []
        RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
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
                RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
                TheReaction = reaction.content()

                reactions_list[str(TheReaction)] += 1

        except requests.exceptions.ReadTimeout as aes:
            raise SystemError('ReadTimeout error in event mining')
        except requests.exceptions.ConnectionError as aes:
            raise SystemError('Connection error in event mining')
        except GithubException as d:
            if (d.status == 403):
                raise SystemError('Request limit achieved in event mining ')

        return pattern.ReactionPattern([reactions_list['+1'],
                                        reactions_list['heart'],
                                        reactions_list['hooray'],
                                        reactions_list['confused'],
                                        reactions_list['-1'],
                                        reactions_list['laugh'],
                                        reactions_list['rocket'],
                                        reactions_list['eyes']
                                        ])

    def repo_labels_mining(self, component):
        issue_labels_list = []
        RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
        pattern = PersistencePattern()

        try:
            for label in component.get_labels():
                issue_labels_list.append(label)
        except requests.exceptions.ReadTimeout as aes:
            raise SystemError('ReadTimeout error in event mining')
        except requests.exceptions.ConnectionError as aes:
            raise SystemError('Connection error in event mining')
        except GithubException as d:
            if (d.status == 403):
                raise SystemError('Request limit achieved in event mining ')

        return pattern.LabelsPattern(issue_labels_list)

    def getLastIssue(self, repo):
        try:
            RequestVerificationClass(self.authentication, self.time_to_wait, self.num_requests)
            repository = self.authentication.get_repo(repo)

            for issue in repository.get_issues(state='all'):
                return int(issue.number)
        except GithubException as d:
            if(d.status == 404):
                raise SystemError('Error 404')
