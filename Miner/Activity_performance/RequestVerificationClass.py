from datetime import time
import requests


class RequestVerificationClass():
    def __init__(self, authentication, limit, time_to_wait):
        self.authentication = authentication
        self.limit = limit
        self.time_to_wait = time_to_wait
        self.requests = self.verify_rate_limit()

        if (self.requests < self.time_to_wait):
            self.wait_until()

    def verify_rate_limit(self):
        try:
            request_amount = int(self.authentication.get_rate_limit().core.remaining)

            return request_amount
        except requests.exceptions.ConnectionError:
            raise SystemError('ConnectionError')

    def wait_until(self):
        while (self.requests < self.limit):
            time.sleep(self.time_to_wait)
            self.requests = self.verify_rate_limit()
