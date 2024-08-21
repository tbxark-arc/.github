import os
import json
import requests

class EnvVars:
    def __init__(self):
        self.access_token = os.getenv("ACCESS_TOKEN")
        if not self.access_token:
            raise Exception("A personal access token is required to proceed!")
        self.user = os.getenv("CUSTOM_ACTOR")
        if self.user is None:
            user = os.getenv("GITHUB_ACTOR")
        if self.user is None:
            raise RuntimeError("Environment variable CUSTOM_ACTOR must be set.")
        exclude_repos = os.getenv("EXCLUDED")
        self.excluded_repos = (
            {x.strip() for x in exclude_repos.split(",")} if exclude_repos else None
        )
        exclude_langs = os.getenv("EXCLUDED_LANGS")
        self.excluded_langs = (
            {x.strip() for x in exclude_langs.split(",")} if exclude_langs else None
        )
        exclud_users = os.getenv("EXCLUDED_USERS")
        self.excluded_users = (
            {x.strip() for x in exclud_users.split(",")} if exclud_users else None
        )
        include_users = os.getenv("INCLUDE_USERS")
        self.included_users = (
            {x.strip() for x in include_users.split(",")} if include_users else None
        )
        # Convert a truthy value to a Boolean
        raw_ignore_forked_repos = os.getenv("EXCLUDE_FORKED_REPOS")
        self.ignore_forked_repos = (
            not not raw_ignore_forked_repos
            and raw_ignore_forked_repos.strip().lower() != "false"
        )

        raw_ignore_archived_repos = os.getenv("EXCLUDE_ARCHIVED_REPOS")
        self.ignore_archived_repos = (
            not not raw_ignore_archived_repos
            and raw_ignore_archived_repos.strip().lower() != "false"
        )

        self.stat_upload_url = os.getenv("STAT_UPLOAD_URL")
        
    def to_dict(self):
        return {
            "access_token": self.access_token,
            "user": self.user,
            "exclude_repos": list(self.excluded_repos) if self.excluded_repos else None,
            "exclude_langs": list(self.excluded_langs) if self.excluded_langs else None,
            "excluded_users": list(self.excluded_users) if self.excluded_users else None,
            "include_users": list(self.included_users) if self.included_users else None,
            "ignore_forked_repos": self.ignore_forked_repos,
            "ignore_archived_repos": self.ignore_archived_repos,
            "stat_upload_url": self.stat_upload_url,
        }
        
 
def main() -> None:
    """
    Generate all badges
    """
    vars = EnvVars()
    json_text = json.dumps(vars.to_dict(), indent=4)
    if vars.stat_upload_url is None:
        raise Exception("Environment variable STAT_UPLOAD")
    r = requests.post(vars.stat_upload_url, data=json_text)
    print(r.status_code)   

if __name__ == "__main__":
    main()
