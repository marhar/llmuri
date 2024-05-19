#!/usr/bin/env python

import unittest
from llmuri import uri_to_litellm


class TestUriToLitellm(unittest.TestCase):

    def zztest_basic_uri_with_prefix(self):
        uri = "llm://modelname"
        expected_output = {"model": "modelname"}
        self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_no_uri_prefix(self):
        test_cases = [
            (
                "aaa/bbb",
                {"model": "bbb"},
            ),
            (
                "llm:aaa/bbb",
                {"model": "bbb"},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_query_parms(self):
        test_cases = [
            (
                "aaa/bbb",
                {"model": "bbb"},
            ),
            (
                "llm:aaa/bbb?",
                {"model": "bbb"},
            ),
            (
                "llm:aaa/bbb?a=1",
                {'a': '1', 'model': 'bbb'}
            ),
            (
                "llm:aaa/bbb?a=1&b=2",
                {'a': '1', 'b': '2', 'model': 'bbb'}
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_fragments(self):
        test_cases = [
            (
                "aaa/bbb",
                {"model": "bbb"},
            ),
            (
                "aaa/bbb#",
                {"model": "bbb#"},
            ),
            (
                "aaa/bbb#foo",
                {"model": "bbb#foo"},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_abbreviations(self):
        test_cases = [
            (
                "mistralai/mistral-medium",
                {'api_base': 'https://api.mistral.ai/v1', 'model': 'mistral-medium'},
            ),
            (
                "openai/gpt-4",
                {'api_base': 'https://api.openai.com/v1', 'model': 'gpt-4'},
            ),
            (
                "ollama/llama2",
                {'api_base': 'http://localhost:11434', 'model': 'ollama/llama2'},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)


if __name__ == "__main__":
    unittest.main()
