import json


class KibanaApiBase(object):
    es = None

    def __init__(self, elastic_search):
        self.es = elastic_search


class KibanaApiModelBase(object):
    @classmethod
    def serialize(cls, data):
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def unserialize(cls, string):
        return json.loads(string)
