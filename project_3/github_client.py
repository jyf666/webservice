import requests
import json


class Client:

    def __init__(self, github_token):
        self.github_token = github_token
        self.session = requests.Session()
        self.session.keep_alive = False
        self.header = {"Authorization": "token " + github_token}
        self.response = self.session.get(
            "https://api.github.com/user", headers=self.header).json()
        self.username = self.response.get("login")

    def list_stars(self):
        if(not self.response.get("message") == "Bad credentials"):
            return self.page_list(self.getURL("starred_url"))
        else:
            raise Exception("invalid credentials")

    def list_followers(self):
        if(not self.response.get("message") == "Bad credentials"):
            return self.page_list(self.getURL("followers_url"))
        else:
            raise Exception("invalid credentials")

    def list_repo(self):
        if(not self.response.get("message") == "Bad credentials"):
            return self.page_list(self.getURL("repos_url"))
        else:
            raise Exception("invalid credentials")

    def star_repo(self, repo_id):
        if(not self.response.get("message") == "Bad credentials"):
            if not type(repo_id) == int:
                raise Exception("an error has occurred")
            exist = 0
            for star in json.loads(self.list_stars()):
                if repo_id == star.get("id"):
                    exist = 1
            if exist == 0:
                status = requests.put(
                    "https://api.github.com/user/starred/{}/{}".format(
                        self.get_reponame(repo_id)[0],
                        self.get_reponame(repo_id)[1]),
                    headers=self.header).status_code
                if status < 300:
                    return json.dumps({"status": "ok"})
                else:
                    raise Exception("an error has occurred")
            else:
                raise Exception("an error has occurred")
        else:
            raise Exception("invalid credentials")

    def follow_user(self, user_id):
        if(not self.response.get("message") == "Bad credentials"):
            if not type(user_id) == int:
                raise Exception("an error has occurred")
            exist = 0
            for followering in json.loads(self.page_list(
                    self.getURL("following_url"))):
                if user_id == followering.get("id"):
                    exist = 1
            if exist == 0:
                status = requests.put(
                    "https://api.github.com/user/following/{}".format(
                        self.get_username(user_id)),
                    headers=self.header).status_code
                if status < 300:
                    return json.dumps({"status": "ok"})
                else:
                    raise Exception("an error has occurred")
            else:
                raise Exception("an error has occurred")
        else:
            raise Exception("invalid credentials")

    def unfollow_user(self, user_id):
        if(not self.response.get("message") == "Bad credentials"):
            if not type(user_id) == int:
                raise Exception("an error has occurred")
            exist = 0
            for followering in json.loads(self.page_list(
                    self.getURL("following_url"))):
                if user_id == followering.get("id"):
                    exist = 1
            if exist == 1:
                status = requests.delete(
                    "https://api.github.com/user/following/{}".format(
                        self.get_username(user_id)),
                    headers=self.header).status_code
                if status < 300:
                    return json.dumps({"status": "ok"})
                else:
                    raise Exception("an error has occurred")
            else:
                raise Exception("an error has occurred")
        else:
            raise Exception("invalid credentials")

    def create_repo(self, name):
        if(not self.response.get("message") == "Bad credentials"):
            new_repo = {'name': name}
            status = requests.post(
                "https://api.github.com/user/repos",
                json=new_repo, headers=self.header).status_code
            if status == 201:
                url = "https://api.github.com/repos/{}/{}".format(
                    self.username, name)
                return json.dumps(requests.get(
                    url, headers=self.header).json())
            else:
                raise Exception("unknown error")
        else:
            raise Exception("invalid credentials")

    def delete_repo(self, repo_id):
        if(not self.response.get("message") == "Bad credentials"):
            if not type(repo_id) == int:
                raise Exception("an error has occurred")
            exist = 0
            for repo in json.loads(self.list_repo()):
                if repo_id == repo.get("id"):
                    exist = 1
            if exist == 1:
                url = "https://api.github.com/repos/{}/{}".format(
                    self.get_reponame(repo_id)[0],
                    self.get_reponame(repo_id)[1])
                status = requests.delete(url, headers=self.header).status_code
                if status < 300:
                    return json.dumps({"status": "ok"})
                else:
                    raise Exception("an error has occurred")
            else:
                raise Exception("an error has occurred")
        else:
            raise Exception("invalid credentials")

    def getURL(self, url_str):
        try:
            validURL = self.response.get(url_str).split("{")[0]
            return validURL
        except Exception as e:
            raise Exception("unknown error")

    def page_list(self, url):
        total = []
        i = 1
        while True:
            param = {"per_page": 100, "page": i}
            page_result = self.session.get(
                url, headers=self.header, params=param).json()
            if len(page_result) == 0:
                break
            total.extend(page_result)
            i += 1
        return json.dumps(total)

    def get_username(self, user_id):
        if user_id <= 0:
            raise Exception("an error has occurred")
        userid = user_id - 1
        result = requests.get(
            "https://api.github.com/users?since={}&per_page=1".format(
                userid),
            headers=self.header).json()
        status = requests.get(
            "https://api.github.com/users?since={}&per_page=1".format(
                userid),
            headers=self.header).status_code
        if (status == 404) or (len(result) == 0)or(
                not result[0].get("id") == user_id):
            raise Exception("an error has occurred")
        else:
            follow_username = result[0].get("login")
            return follow_username

    def get_reponame(self, repo_id):
        if repo_id <= 0:
            raise Exception("an error has occurred")
        repoid = repo_id - 1
        result = requests.get(
            "https://api.github.com/repositories?since={}".format(
                repoid), headers=self.header).json()
        status = requests.get(
            "https://api.github.com/repositories?since={}".format(
                repoid), headers=self.header).status_code
        if (status == 404) or (len(result) == 0)or(
                not result[0].get("id") == repo_id):
            raise Exception("an error has occurred")
        else:
            repo_name = result[0].get("name")
            owner_name = result[0].get("owner").get("login")
            return owner_name, repo_name
