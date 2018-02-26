from elasticsearch import Elasticsearch
from . import keywordContentRepo
from commonLink import models
from var_dump import var_export


class KeywordContentES(object):
    def __init__(self):
        self.es_client = Elasticsearch(hosts=["127.0.0.1"])
        self.index = 'freelink'
        self.doc_type = 'keywordContent'

    def create(self):
        return self.es_client.indices.create(
            index=self.index,
            body={
                'mappings': {
                    self.doc_type: {
                        'properties': {
                            'id_keyword': {
                                'type': 'keyword'
                            },
                            'id_content': {
                                'type': 'keyword'
                            },
                            'keyword': {
                                'type': 'text',
                                'analyzer': 'ik_max_word'
                            },
                            'content': {
                                'type': 'text',
                                'analyzer': 'ik_max_word'
                            }
                        }
                    }
                }
            }
        )

    def indexAll(self):
        result = []
        for data in self.keywordContentBulkData():
            temp = self.bulk(data)
            if temp['errors']:
                return temp
        return 'all right'

    def bulk(self, sourceData):
        return self.es_client.bulk(
            index=self.index,
            doc_type=self.doc_type,
            body=sourceData,
            refresh=True
        )

    def keywordContentBulkData(self):
        data = []
        for keywords in self.getKeywordIds():
            for k in keywords:
                line = keywordContentRepo.get_keyword_content(k.id)
                data.append({
                    "index": {
                        "_index": self.index,
                        "_type": self.doc_type,
                        "_id": line['keyword'].id
                    }
                })
                data.append({
                    'id_keyword':line['keyword'].id,
                    'id_content':line['content'].id,
                    'keyword':line['keyword'].keyword,
                    'content':line['content'].content
                })
            yield data
            data = []

    def getKeywordIds(self):
        offset = 0
        while True:
            limit = offset + 10
            keywords = models.keyword.objects.all()[offset:limit]
            if keywords:
                yield keywords
                offset += 5
            else:
                break


    def searchKeyword(self, keyword):
        return self.es_client.search(
            index=self.index,
            doc_type=self.doc_type,
            body={
                "query":{
                    "multi_match":{
                        "query": keyword,
                        "fields": ["keyword^1.3", "content"]
                    }
                },
                "from": 0,
                "size": 300,
                "highlight": {
                    "pre_tags" : ["<span class='em'>"],
                    "post_tags" : ["</span>"],
                    "fields": {
                        "keyword": {},
                        "content": {}
                    }
                }
            }
        )
