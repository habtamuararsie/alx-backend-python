#!/usr/bin/env python3
""" Module for testing utils """

from parameterized import parameterized
import unittest
from unittest.mock import patch
from utils import (access_nested_map, get_json, memoize)
import requests


class TestAccessNestedMap(unittest.TestCase):
    """ Class for Testing Access Nested Map """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test that the method returns what it is supposed to """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """ Test that a KeyError is raised for the respective inputs """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(e.exception))


class TestGetJson(unittest.TestCase):
    """ Class for Testing Get Json """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """ Test that utils.get_json returns the expected result."""
        config = {'return_value.json.return_value': test_payload}
        patcher = patch('requests.get', **config)
        mock = patcher.start()
        self.assertEqual(get_json(test_url), test_payload)
        mock.assert_called_once()
        patcher.stop()


class TestMemoize(unittest.TestCase):
    """ Class for Testing Memoize """

    def test_memoize(self):
        """ Test that when calling a_property twice, the correct result
        is returned but a_method is only called once using
        assert_called_once
        """

        class TestClass:
            """ Test Class for wrapping with memoize """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock.assert_called_once()
# #!/usr/bin/env python3
# """ Parameterize a unit test, Mock HTTP calls, Parameterize and patch """
# import unittest
# from unittest.mock import patch
# from parameterized import parameterized
# from utils import access_nested_map, get_json, memoize
# from typing import (
#     Mapping,
#     Sequence,
#     Any,
#     Dict,
#     Callable,
# )

# class TestAccessNestedMap(unittest.TestCase):
#     """ TESTCASE """
#     """ to test the function for following inputs """
#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, answer):
#         """ method to test that the method returns what it is supposed to """
#         self.assertEqual(access_nested_map(nested_map, path), answer)

#     """  to test that a KeyError is raised for the following inputs """
#     @parameterized.expand([
#         ({}, ("a",)),
#         ({"a": 1}, ("a", "b")),
#     ])
#     def test_access_nested_map_exception(self, nested_map, path):
#         """ method to test that a KeyError is raised properly """
#         with self.assertRaises(KeyError) as error:
#             access_nested_map(nested_map, path)
#         self.assertEqual(error.exception.args[0], path[-1])


# class TestGetJson(unittest.TestCase):
#     """ TESTCASE """
#     """ to test the function for following inputs """
#     @parameterized.expand([
#         ("http://example.com", {"payload": True}),
#         ("http://holberton.io", {"payload": False}),
#     ])
#     @patch('test_utils.get_json')
#     def test_get_json(self, test_url, test_payload, mock_get):
#         """ method to test that utils.get_json returns the expected result """
#         mock_get.return_value = test_payload
#         result = get_json(test_url)
#         self.assertEqual(result, test_payload)


# class TestMemoize(unittest.TestCase):
#     """ TESTCASE """

#     def test_memoize(self):
#         """ Test that when calling a_property twice
#         """
#         class TestClass:
#             """ class """

#             def a_method(self):
#                 """ method  """

#                 return 42

#             @memoize
#             def a_property(self):
#                 """ property """
#                 return self.a_method()
#         with patch.object(TestClass, "a_method") as mockMethod:
#             test_class = TestClass()
#             test_class.a_property
#             test_class.a_property
#             mockMethod.assert_called_once
