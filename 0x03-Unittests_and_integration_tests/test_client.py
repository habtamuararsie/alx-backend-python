# #!/usr/bin/env python3
# """ Parameterize and patch as decorators, Mocking a property, More patching,
#     Parameterize, Integration test: fixtures, Integration tests """
# import unittest
# from unittest.mock import patch, PropertyMock, Mock
# from parameterized import parameterized
# from client import GithubOrgClient
# from fixtures import TEST_PAYLOAD
# from urllib.error import HTTPError


# class TestGithubOrgClient(unittest.TestCase):
#     """ TESTCASE inputs to test the functionality
#       """

#     @parameterized.expand([
#         ("google"),   ("abc"),
#     ])
#     @patch("client.get_json", return_value={"payload": True})

#     def test_org(self, org_name, mock_get):
#         """ test that GithubOrgClient.org method
#           """
#         test_client = GithubOrgClient(org_name)
#         test_return = test_client.org
#         self.assertEqual(test_return, mock_get.return_value)
#         mock_get.assert_called_once

#     def test_public_repos_url(self):
#         """ to unit-test GithubOrgClient._public_repos_url """
#         with patch.object(GithubOrgClient,
#                           "org",
#                           new_callable=PropertyMock,
#                           return_value={"repos_url": "holberton"}) as mock_get:
#             test_json = {"repos_url": "holberton"}
#             test_client = GithubOrgClient(test_json.get("repos_url"))
#             test_return = test_client._public_repos_url
#             mock_get.assert_called_once
#             self.assertEqual(test_return,
#                              mock_get.return_value.get("repos_url"))

#     @patch("client.get_json", return_value=[{"name": "holberton"}])
#     def test_public_repos(self, mock_get):
#         """ to unit-test GithubOrgClient.public_repos """
#         with patch.object(GithubOrgClient,
#                           "_public_repos_url",
#                           new_callable=PropertyMock,
#                           return_value="https://api.github.com/") as mock_pub:
#             test_client = GithubOrgClient("hoberton")
#             test_return = test_client.public_repos()
#             self.assertEqual(test_return, ["holberton"])
#             mock_get.assert_called_once
#             mock_pub.assert_called_once

#     """ inputs to test the functionality """
#     @parameterized.expand([
#         ({"license": {"key": "my_license"}}, "my_license", True),
#         ({"license": {"key": "other_license"}}, "my_license", False),
#     ])
#     def test_has_license(self, repo, license_key, expected_return):
#         """ to unit-test GithubOrgClient.has_license """
#         test_client = GithubOrgClient("holberton")
#         test_return = test_client.has_license(repo, license_key)
#         self.assertEqual(expected_return, test_return)


# @parameterized_class(
#     ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
#     TEST_PAYLOAD
# )
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """ TESTCASE """
#     @classmethod
#     def setUpClass(cls):
#         """ It is part of the unittest.TestCase API
#         method to return example payloads found in the fixtures """
#         cls.get_patcher = patch('requests.get', side_effect=HTTPError)

#     @classmethod
#     def tearDownClass(cls):
#         """ It is part of the unittest.TestCase API
#         method to stop the patcher """
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         """ method to test GithubOrgClient.public_repos """
#         test_class = GithubOrgClient("holberton")
#         assert True

#     def test_public_repos_with_license(self):
#         """ method to test the public_repos with the argument license """
#         test_class = GithubOrgClient("holberton")
#         assert True

#!/usr/bin/env python3

""" Tests for client
"""

import unittest
import requests
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import Mock, patch, PropertyMock
from utils import get_json
from client import GithubOrgClient
import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ Test class for GithubOrgClient
    """

    @parameterized.expand(
        [("google", {"google", True}), ("abc", {"abc", True})])
    @patch('client.get_json')
    def test_org(self, org, expected, get_patch):
        """ Test the GithubOrgClient.org method
        """
        get_patch.return_value = expected
        gh_client = GithubOrgClient(org)
        self.assertEqual(gh_client.org, expected)
        get_patch.assert_called_once_with(f'https://api.github.com/orgs/{org}')

    def test_public_repos_url(self):
        """ Test the GithubOrgClient._public_repos_url
        """
        expected = "www.geoff.com"
        with patch('client.GithubOrgClient.org',
                   PropertyMock(return_value={'repos_url': expected})):
            gh_client = GithubOrgClient("adobe")
            self.assertEqual(gh_client._public_repos_url, expected)

    """ @patch('client.get_json')
    def test_public_repos(self, get_patch):
        repo1={"license1": {"key": "my_license"}},
        repo2={"license2": {"key": "other_license"}}
        get_patch.return_value = [repo1, repo2]
        with patch('client.GithubOrgClient._public_repos_url',
        PropertyMock(return_value={'www.geoff.com'})) as mock:
            gh_client = GithubOrgClient('adobe')
            self.assertEqual(gh_client.public_repos(), ['repo1', 'repo2'])
            self.assertEqual(gh_client.public_repos('a'), ['geoff'])
            get_json.assert_called_once_with('www.geoff.com')
            mock.assert_called_once_with() """

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)])
    def test_has_license(self, repo, license_key, expected):
        """ Test GithubOrgClient.has_license method
        """
        self.assertEqual(
            GithubOrgClient.has_license(
                repo, license_key), expected)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Test class for GithubOrgClient.public_repos
    """

    @classmethod
    def setUpClass(cls):
        """ Setup tests for class GithubOrgClient
        """
        pass

    def tearDownClass(self):
        """ Teardown tests for GithubOrgClient
        """
        pass

    def test_public_repos_with_license(self):
        """ Test GithubOrgClient.public_repos method
        """
        pass

    def test_public_repos(self):
        """ Test GithubOrgClient.public_repos method
        """
        pass

    def test_public_repos_with_license(self):
        """ Test public_repos
        """
        pass
