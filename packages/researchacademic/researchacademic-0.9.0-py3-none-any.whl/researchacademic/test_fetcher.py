import os
import unittest
import json

from fetcher import EntityParser as EP
from fetcher import ResearchAcademic as RA

API_KEY = os.environ["MICROSOFT_API_KEY"]


class TestEntityParser(unittest.TestCase):
    def setUp(self):
        with open('researchacademic/entity.json') as json_file:
            self.entity = json.load(json_file)
            self.ep = EP(self.entity)

    def test_parse_abstract(self):
        abstract = self.ep.parse_abstract()
        abstract = abstract["abstract"][2:23]
        self.assertEqual(abstract, "The production effect")

    def test_parse_result(self):
        result = self.ep.parse_result()
        assert result["year"] == 2012
        assert result["doi"] == "10.1037/A0028466"
        assert result["authors"][0]["authorId"] == 2047873968


class TestResearchAcademic(unittest.TestCase):
    def setUp(self):
        self.ra = RA(API_KEY)

    def test_parse_query(self):
        parsed_query = self.ra.parse_query('10.1037/A0028466')

        expr = parsed_query["expr"]
        self.assertEqual(expr, "DOI='10.1037/A0028466'")
        parsed_query = self.ra.parse_query(
            'Information revelation and privacy in online social networks')
        expr = parsed_query["expr"]
        self.assertEqual(
            expr,
            "Ti='information revelation and privacy in online social networks'"
        )

    def test_evaluate(self):
        results = self.ra.evaluate("10.1037/A0028466", timeout=5)
        result = results[0]
        self.assertEqual(result["doi"], "10.1037/A0028466")


if __name__ == '__main__':
    unittest.main()
