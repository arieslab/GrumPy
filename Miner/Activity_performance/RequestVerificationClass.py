import time
import requests
import github
from datetime import time
from requests import exceptions
from github import Github, GithubException


class VerificationClass:
    def __init__(self, authentication, limit, time_to_wait):
        self.authentication = authentication
        self.limit = limit
        self.time_to_wait = time_to_wait
        self.Requests_Amount = 30

        if (self.Requests_Amount < self.time_to_wait):
            self.wait_until()

    def verify_rate_limit(self):
        try:
            self.Requests_Amount = int(self.authentication.get_rate_limit().core.remaining)

            return self.Requests_Amount
        except requests.exceptions.ConnectionError:
            raise SystemError('ConnectionError')

    def wait_until(self):
        while (self.Requests_Amount < self.limit):
            time.sleep(self.time_to_wait)
            self.Requests_Amount = self.verify_rate_limit()