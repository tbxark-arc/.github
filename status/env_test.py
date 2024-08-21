import os
import asyncio
import json
import requests

def main() -> None:
    """
    Generate all badges
    """
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        # access_token = os.getenv("GITHUB_TOKEN")
        raise Exception("A personal access token is required to proceed!")
    user = os.getenv("CUSTOM_ACTOR")
    if user is None:
        user = os.getenv("GITHUB_ACTOR")
    if user is None:
        raise RuntimeError("Environment variable CUSTOM_ACTOR must be set.")
    exclude_repos = os.getenv("EXCLUDED")
    excluded_repos = (
        {x.strip() for x in exclude_repos.split(",")} if exclude_repos else None
    )
    exclude_langs = os.getenv("EXCLUDED_LANGS")
    excluded_langs = (
        {x.strip() for x in exclude_langs.split(",")} if exclude_langs else None
    )
    excluded_users = os.getenv("EXCLUDED_USERS")
    excluded_users = (
        {x.strip() for x in excluded_users.split(",")} if excluded_users else None
    )
    include_users = os.getenv("INCLUDE_USERS")
    include_users = (
        {x.strip() for x in include_users.split(",")} if include_users else None
    )
    # Convert a truthy value to a Boolean
    raw_ignore_forked_repos = os.getenv("EXCLUDE_FORKED_REPOS")
    ignore_forked_repos = (
        not not raw_ignore_forked_repos
        and raw_ignore_forked_repos.strip().lower() != "false"
    )

    raw_ignore_archived_repos = os.getenv("EXCLUDE_ARCHIVED_REPOS")
    ignore_archived_repos = (
        not not raw_ignore_archived_repos
        and raw_ignore_archived_repos.strip().lower() != "false"
    )

    stat_upload_url = os.getenv("STAT_UPLOAD_URL")
    if stat_upload_url is None:
            raise Exception("Environment variable STAT_UPLOAD")
        
    report = {
        "access_token": access_token,
        "user": user,
        "exclude_repos": list(excluded_repos),
        "exclude_langs": list(excluded_langs),
        "excluded_users": list(excluded_users),
        "include_users": list(include_users),
        "ignore_forked_repos": ignore_forked_repos,
        "ignore_archived_repos": ignore_archived_repos,
        "stat_upload_url": stat_upload_url,
    }

    json_text = json.dumps(report, indent=4)
    r = requests.post(stat_upload_url, data=json_text)
    print(r.status_code)
    

if __name__ == "__main__":
    main()
