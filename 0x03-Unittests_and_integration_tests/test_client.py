# #!/usr/bin/env python3
# """ Parameterize and patch as decorators, Mocking a property, More patching,
#     Parameterize, Integration test: fixtures, Integration tests """
# import unittest
# import client
# from utils import get__json
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
""" Test the utils """


import requests
import unittest
from unittest.mock import patch, Mock, PropertyMock, call
from parameterized import parameterized, parameterized_class
import utils
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient
import client
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ Test that json can be got """

    @parameterized.expand([
        ("google", {"google": True}),
        ("abc", {"abc": True})
    ])
    @patch('client.get_json')
    def test_org(self, org, expected, get_patch):
        """ Test the org of the client """
        get_patch.return_value = expected
        x = GithubOrgClient(org)
        self.assertEqual(x.org, expected)
        get_patch.assert_called_once_with("https://api.github.com/orgs/"+org)

    def test_public_repos_url(self):
        """ test that _public_repos_url works """
        expected = "www.yes.com"
        payload = {"repos_url": expected}
        to_mock = 'client.GithubOrgClient.org'
        with patch(to_mock, PropertyMock(return_value=payload)):
            cli = GithubOrgClient("x")
            self.assertEqual(cli._public_repos_url, expected)

    @patch('client.get_json')
    def test_public_repos(self, get_json_mock):
        """ test the public repos """
        jeff = {"name": "Jeff", "license": {"key": "a"}}
        bobb = {"name": "Bobb", "license": {"key": "b"}}
        suee = {"name": "Suee"}
        to_mock = 'client.GithubOrgClient._public_repos_url'
        get_json_mock.return_value = [jeff, bobb, suee]
        with patch(to_mock, PropertyMock(return_value="www.yes.com")) as y:
            x = GithubOrgClient("x")
            self.assertEqual(x.public_repos(), ['Jeff', 'Bobb', 'Suee'])
            self.assertEqual(x.public_repos("a"), ['Jeff'])
            self.assertEqual(x.public_repos("c"), [])
            self.assertEqual(x.public_repos(45), [])
            get_json_mock.assert_called_once_with("www.yes.com")
            y.assert_called_once_with()

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    def test_has_license(self, repo, license, expected):
        """ test the license checker """
        self.assertEqual(GithubOrgClient.has_license(repo, license), expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test for github org client """

    @classmethod
    def setUpClass(cls):
        """ prepare for testing """
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        cls.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        cls.repos_mock = repos_mock

        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()

        options = {cls.org_payload["repos_url"]: repos_mock}
        cls.get.side_effect = lambda y: options.get(y, org_mock)

    @classmethod
    def tearDownClass(cls):
        """ unprepare for testing """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ public repos test """
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])

    def test_public_repos_with_license(self):
        """ public repos test """
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.assertEqual(y.public_repos("apache-2.0"), self.apache2_repos)
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])
