import requests
import sys
from requests import exceptions
from github import Github, GithubException

class MinersClass():
    def __init__(self, issue, authentication):
        self.issue = issue
        self.authentication = authentication

    