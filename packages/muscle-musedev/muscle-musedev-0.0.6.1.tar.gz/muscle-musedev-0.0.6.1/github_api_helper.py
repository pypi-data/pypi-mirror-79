import requests

DEFAULT_SUPPORTED_LANGUAGES = ["Java", "JavaScript", "Python", "C", "C++"]

def getSupportedRepos(owner):
    r = requests.get(f'https://api.github.com/orgs/{owner}/repos')
    return [repo["name"] for repo in r.json() if repo["language"] in DEFAULT_SUPPORTED_LANGUAGES]
