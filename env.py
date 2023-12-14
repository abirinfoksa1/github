"""
Sets up the environment variables for the action.
"""

import os
from os.path import dirname, join

from dotenv import load_dotenv


def get_env_vars() -> (
    tuple[str | None, list[str], str, str, list[str], str, str, str, int | None]
):
    """
    Get the environment variables for use in the action.

    Args:
        None

    Returns:
        str: the organization to get contributor information for
        List[str]: A list of the repositories to get contributor information for
        str: the GitHub token to use for authentication
        str: the GitHub Enterprise URL to use for authentication
        str: the start date to get contributor information from
        str: the end date to get contributor information to.
        str: whether to get sponsor information on the contributor

    """
    # Load from .env file if it exists
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    organization = os.getenv("ORGANIZATION")
    repositories_str = os.getenv("REPOSITORY")
    # Either organization or repository must be set
    if not organization and not repositories_str:
        raise ValueError(
            "ORGANIZATION and REPOSITORY environment variables were not set. Please set one"
        )

    if repositories_str and repositories_str.find("/") == 0:
        raise ValueError(
            "REPOSITORY environment variable was not set correctly. Please set it to a comma separated list of repositories in the format org/repo"
        )

    # Separate repositories_str into a list based on the comma separator
    repositories_list = []
    if repositories_str:
        repositories_list = [
            repository.strip() for repository in repositories_str.split(",")
        ]

    token = os.getenv("GH_TOKEN")
    # required env variable
    if not token:
        raise ValueError("GH_TOKEN environment variable not set")

    ghe = os.getenv("GH_ENTERPRISE_URL", default="").strip()

    exempt_repos = os.getenv("EXEMPT_REPOS")
    exempt_repositories_list = []
    if exempt_repos:
        exempt_repositories_list = [
            repository.strip() for repository in exempt_repos.split(",")
        ]

    follow_up_type = os.getenv("TYPE")
    # make sure that follow_up_type is either "issue" or "pull"
    if follow_up_type:
        if follow_up_type not in ("issue", "pull"):
            raise ValueError("TYPE environment variable not 'issue' or 'pull'")
    else:
        follow_up_type = "pull"

    title = os.getenv("TITLE")
    # make sure that title is a string with less than 70 characters
    if title:
        if len(title) > 70:
            raise ValueError("TITLE environment variable is too long")
    else:
        title = "Enable Dependabot"

    body = os.getenv("BODY")
    # make sure that body is a string with less than 65536 characters
    if body:
        if len(body) > 65536:
            raise ValueError("BODY environment variable is too long")
    else:
        body = "Dependabot could be enabled for this repository. \
Please enable it by merging this pull request \
so that we can keep our dependencies up to date and secure."

    created_after_date = os.getenv("CREATED_AFTER_DATE")
    # make sure that created_after_date is a date in the format YYYY-MM-DD
    if created_after_date and len(created_after_date) != 10:
        raise ValueError("CREATED_AFTER_DATE environment variable not in YYYY-MM-DD")

    return (
        organization,
        repositories_list,
        token,
        ghe,
        exempt_repositories_list,
        follow_up_type,
        title,
        body,
        created_after_date,
    )
