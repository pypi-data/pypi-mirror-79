import requests

ON_DEMAND_API_BASE_URL="https://production.muse.dev/api/v1/on-demand"

# Params: URL encoded owner, repo and branch name
def branch_to_hash(owner, repo, branch):
    r = requests.get(f'https://api.github.com/repos/{owner}/{repo}/branches/{branch}')
    return r.json()["commit"]["sha"]

def post_analyze(jwt, owner, repo, commit):
    repo_url = f"https://github.com/{owner}/{repo}"
    payload = {'jwt': jwt, 'commitHash': commit, 'repoUrl': repo_url}
    r = requests.post(ON_DEMAND_API_BASE_URL + '/analyze', params=payload)
    return r.text

def get_status(jwt, job_id):
    payload = {'jwt': jwt, 'jobId': job_id}
    r = requests.get(ON_DEMAND_API_BASE_URL + '/getStatus', params=payload)
    return r.text

def get_results(jwt, job_id):
    payload = {'jwt': jwt, 'jobId': job_id}
    r = requests.get(ON_DEMAND_API_BASE_URL + '/getResults', params=payload)
    return r.json()