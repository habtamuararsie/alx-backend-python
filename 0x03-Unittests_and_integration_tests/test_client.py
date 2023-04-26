#!/usr/bin/env python3
""" Module for testing client """

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import json
import unittest
from unittest.mock import patch, PropertyMock, Mock


class TestGithubOrgClient(unittest.TestCase):
    """ Class for Testing Github Org Client """

    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, input, mock):
        """Test that GithubOrgClient.org returns the correct value"""
        test_class = GithubOrgClient(input)
        test_class.org()
        mock.assert_called_once_with(f'https://api.github.com/orgs/{input}')

    def test_public_repos_url(self):
        """ Test that the result of _public_repos_url is the expected one
        based on the mocked payload
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            payload = {"repos_url": "World"}
            mock.return_value = payload
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        """
        Test that the list of repos is what you expect from the chosen payload.
        Test that the mocked property and the mocked get_json was called once.
        """
        json_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public:

            mock_public.return_value = "hello/world"
            test_class = GithubOrgClient('test')
            result = test_class.public_repos()

            check = [i["name"] for i in json_payload]
            self.assertEqual(result, check)

            mock_public.assert_called_once()
            mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ unit-test for GithubOrgClient.has_license """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    
    """ Class for Integration test of fixtures """

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        # def my_side_effect(url):
        #     """ Side Effect function for test """
        #     test_url = "https://api.github.com/orgs/google"
        #     if url == test_url:
        #         return cls.org_payload
        #     return cls.repos_payload

        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ Integration test for public repos with License """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()
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
