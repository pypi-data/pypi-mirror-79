import requests
import json


class ResearchAcademic(object):
    def __init__(self, api_key):
        self.count = 10
        self.offset = 0
        self.attributes = "DOI,DN,Id,J.JN,Y,V,I,IA,AA.AuId,AA.DAuN"
        self.api_key = api_key
        self.base_url = ("https://api.labs.cognitive.microsoft.com/"
                         "academic/v1.0")
        self.timeout = 3
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json"
        }

        self.data = {
            "model": "latest",
            "count": self.count,
            "offset": self.offset,
            "attributes": self.attributes
        }

    @staticmethod
    def parse_query(query):
        if "doi" in query:
            doi = query["doi"]
            return {
                 "expr": f"DOI='{doi}'"
            }

        elif "title" in query:
            title = query["title"]
            title = title.lower()
            return {
                 "expr": f"Ti='{title}'"
            }

    def evaluate(self, query, timeout=None, attributes=None):
        if not timeout:
            timeout = self.timeout

        if not attributes:
            attributes = self.attributes

        url = self.base_url + "/evaluate"

        parsed_query = ResearchAcademic.parse_query(query)
        data = {**self.data, **parsed_query}

        rsp = requests.post(url,
                            headers=self.headers,
                            json=data,
                            timeout=timeout)
        content = json.loads(rsp.content)
        entities = content["entities"]
        results = []
        for origina_entity in entities:
            entity = EntityParser(origina_entity)
            results.append(entity.parse_result())

        return results


class EntityParser(object):
    def __init__(self, entity):
        self.entity = entity

    def parse_abstract(self):
        entity = self.entity
        inverted_abstract = entity.pop("IA")
        index_length = inverted_abstract["IndexLength"]
        inverted_index = inverted_abstract["InvertedIndex"]
        abstract = [""] * index_length

        for word, indexes in inverted_index.items():
            for i in indexes:
                abstract[i] = word

        abstract = " ".join(abstract)

        return {"abstract": abstract}

    def parse_result(self):
        abstract = self.parse_abstract()
        result = EntityParser.parse_entity(self.entity)
        return {**result, **abstract}

    @staticmethod
    def parse_entity(entity):
        '''
        "DOI": "10.1037/A0028466",
            "V": "38",
            "I": "6",
            "AA": [
                {
                    "DAuN": "Glen E. Bodner",
                    "AuId": 2047873968
                },
                {
                    "DAuN": "Alexander Taikh",
                    "AuId": 2333340810
                }
            ],
            "J": {
                "JN": "journal of experimental psychology memory and cognition"
            },
            "IA": {
                "IndexLength": 137,
                "InvertedIndex": {
                "2": [
                        75
                    ],
                    ":": [
                        0
                    ],
                    "The": [
                        1
                    ]
                }
            }
        '''
        matches = {
            "Y": "year",
            "DN": "title",
            "DOI": "doi",
            "V": "volume",
            "I": "issue",
            "AA": "authors",
            "DAuN": "name",
            "AuId": "authorId",
            "J": "journal",
            "JN": "name",
        }
        result = {}
        for key, value in entity.items():
            replaced_key = matches.get(key)
            if not replaced_key:
                continue

            if type(value) in (str, int):
                new_value = value

            elif type(value) == list:
                new_value = []
                for v in value:
                    new_value.append(EntityParser.parse_entity(v))
                value = new_value

            elif type(value) == dict:
                new_value = EntityParser.parse_entity(value)

            else:
                print(replaced_key, value)

            result[replaced_key] = new_value
        return result
