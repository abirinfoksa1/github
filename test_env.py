"""Test the get_env_vars function"""
import unittest
from unittest.mock import patch
import os

from env import get_env_vars


class TestEnv(unittest.TestCase):
    """Test the get_env_vars function"""

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "my_organization",
            "GH_TOKEN": "my_token",
            "EXEMPT_REPOS": "repo4,repo5",
            "TYPE": "issue",
            "TITLE": "Dependabot Alert custom title",
            "BODY": "Dependabot custom body",
            "CREATED_AFTER_DATE": "2023-01-01",
        },
    )
    def test_get_env_vars_with_org(self):
        """Test that all environment variables are set correctly using an organization"""
        expected_result = (
            "my_organization",
            [],
            "my_token",
            "",
            ["repo4", "repo5"],
            "issue",
            "Dependabot Alert custom title",
            "Dependabot custom body",
            "2023-01-01",
        )
        result = get_env_vars()
        self.assertEqual(result, expected_result)

    @patch.dict(
        os.environ,
        {
            "REPOSITORY": "org/repo1,org2/repo2",
            "GH_TOKEN": "my_token",
            "EXEMPT_REPOS": "repo4,repo5",
            "TYPE": "pull",
            "TITLE": "Dependabot Alert custom title",
            "BODY": "Dependabot custom body",
            "CREATED_AFTER_DATE": "2023-01-01",
        },
        clear=True,
    )
    def test_get_env_vars_with_repos(self):
        """Test that all environment variables are set correctly using a list of repositories"""
        expected_result = (
            None,
            ["org/repo1", "org2/repo2"],
            "my_token",
            "",
            ["repo4", "repo5"],
            "pull",
            "Dependabot Alert custom title",
            "Dependabot custom body",
            "2023-01-01",
        )
        result = get_env_vars()
        self.assertEqual(result, expected_result)

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "my_organization",
            "GH_TOKEN": "my_token",
        },
    )
    def test_get_env_vars_optional_values(self):
        """Test that optional values are set to their default values if not provided"""
        expected_result = (
            "my_organization",
            [],
            "my_token",
            "",
            [],
            "pull",
            "Enable Dependabot",
            "Dependabot could be enabled for this repository. \
Please enable it by merging this pull request so that \
we can keep our dependencies up to date and secure.",
            None,
        )
        result = get_env_vars()
        self.assertEqual(result, expected_result)

    @patch.dict(os.environ, {})
    def test_get_env_vars_missing_org_or_repo(self):
        """Test that an error is raised if required environment variables are not set"""
        with self.assertRaises(ValueError):
            get_env_vars()

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "my_organization",
        },
        clear=True,
    )
    def test_get_env_vars_missing_token(self):
        """Test that an error is raised if required environment variables are not set"""
        with self.assertRaises(ValueError):
            get_env_vars()


if __name__ == "__main__":
    unittest.main()
