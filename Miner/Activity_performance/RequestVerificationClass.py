import requests
from requests import exceptions
from github import Github, GithubException


class RequestVerificationClass():
    def __init__(self, authentication, limit):
        self.authentication = authentication
        self.limit = limit

    def verify_rate_limit(self):
        try:
            request_amount = int(self.authentication.get_rate_limit().core.remaining)

            if (request_amount < self.limit):
                return 'Wait '
            else:
                return 'Free to go'
        except requests.exceptions.ConnectionError:
            raise SystemError('ConnectionError')
