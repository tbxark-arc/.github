import asyncio
import os
from typing import Dict, List, Optional, Set, Tuple, Any, cast

import aiohttp
import requests
import json
from github_stats import Stats
from generate_images import generate_languages, generate_overview

async def main() -> None:
    """
    Used mostly for testing; this module is not usually run standalone
    """
    with open('config.json', 'r') as f:
        config = json.load(f)
        async with aiohttp.ClientSession() as session:
            s = Stats(
                config['username'],
                config['access_token'],
                session,
                exclude_repos=config['exclude_repos'],
                exclude_langs=config['exclude_langs'],
                exclude_users=config['exclude_users'],
                include_users=config['include_users'],
                ignore_forked_repos=config['ignore_forked_repos'],
                ignore_archived_repos=config['ignore_archived_repos'],
                stat_url=config['stat_upload_url'],
            )
            await asyncio.gather(generate_languages(s), generate_overview(s))

if __name__ == "__main__":
    asyncio.run(main())
