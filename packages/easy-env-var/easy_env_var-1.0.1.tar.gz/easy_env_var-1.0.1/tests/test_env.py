import os
import unittest
from decimal import Decimal

from easy_env_var import PARSE_MAP, env


class TestCase(unittest.TestCase):
    def tearDown(self) -> None:
        super().tearDown()
        os.environ.pop("foo", None)

    def test_returns_environment_variable(self):
        os.environ["foo"] = "bar"
        self.assertEqual(env("foo"), "bar")

    def test_throws_key_error_if_environment_variable_is_not_set(self):
        with self.assertRaises(KeyError):
            env("foo")

    def test_returns_default_if_environment_variable_is_not_set(self):
        self.assertEqual(env("foo", default="baz"), "baz")

    def test_returns_correct_expected_type(self):
        test_cases = [
            (list, '[1, 2, "a", "b"]', [1, 2, "a", "b"]),
            (dict, '{"a": 1, "2": "b"}', {"a": 1, "2": "b"}),
            (int, "1", 1),
            (float, "1.242", 1.242),
            (str, "bar", "bar"),
            (Decimal, "1.333333", Decimal("1.333333")),
            (bool, "true", True),
        ]
        for _type, var, expected in test_cases:
            os.environ["foo"] = var
            with self.subTest(f"test_{_type.__name__}"):
                self.assertEqual(env("foo", expected_type=_type), expected)

        with self.subTest("test_all_types_are_tested"):
            self.assertEqual(len(test_cases), len(PARSE_MAP))

    def test_different_bool_values(self):
        for boolean in (True, False):
            for op in (str.lower, str.upper, str.title):
                var = op(str(boolean))
                os.environ["foo"] = var
                with self.subTest(f"test_{var}"):
                    self.assertEqual(env("foo", expected_type=bool), boolean)
