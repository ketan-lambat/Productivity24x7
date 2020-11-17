from requests_oauthlib import OAuth2Session

GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""
GITHUB_REDIRECT_URI = "http://localhost:8000/auth/oauth/github"
GITHUB_BASE_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'


def get_github_auth_url():
    github = OAuth2Session(client_id=GITHUB_CLIENT_ID,
                           scope=["read:user", "user:email"])
    auth_url, state = github.authorization_url(GITHUB_BASE_AUTH_URL)
    return auth_url, state


def verify_github(url, state):
    github = OAuth2Session(GITHUB_CLIENT_ID, state=state)
    github.fetch_token(GITHUB_TOKEN_URL, client_secret=GITHUB_CLIENT_SECRET,
                       authorization_response=url)

    return github.get('https://api.github.com/user/emails').json()
