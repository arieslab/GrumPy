import time
import requests
import github
from requests import exceptions
from github import Github, GithubException
from time import sleep

class VerificationClass:
    def __init__(self, authentication, limit, time_to_wait):
        self.authentication = authentication
        self.limit = limit
        self.time_to_wait = time_to_wait
        self.Requests_Amount = self.verify_rate_limit()

        print('Verifying... Nº of Requests '+str(self.Requests_Amount))

        if (self.Requests_Amount < self.time_to_wait):
            self.wait_until()

    def verify_rate_limit(self):
        try:
            self.Requests_Amount = int(self.authentication.get_rate_limit().core.remaining)

            return self.Requests_Amount
        except requests.exceptions.ConnectionError:
            raise SystemError('ConnectionError')

    def wait_until(self):
        print('Verificando... ')
        while (self.Requests_Amount < self.limit):
            print('Requests: ' + str(self.Requests_Amount) + ' Limit: ' + str(self.limit))
            sleep(self.time_to_wait)
            self.Requests_Amount = self.verify_rate_limit()