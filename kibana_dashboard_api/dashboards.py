from .common import KibanaApiModelBase, KibanaApiBase
import uuid


class Dashboard(KibanaApiModelBase):
    """
    Kibana Dashboard model
    """
    id = None
    title = None
    hits = 0
    description = None
    panels = None
    options = None
    ui_state = None
    version = 1
    time_restore = True
    time_to = "now"
    time_from = "now-7d"
    refresh_interval_value = 0
    search_source = None

    @classmethod
    def from_kibana(cls, es_document):
        if es_document.get('_type') != 'dashboard':
            raise Exception('The document is not a dashboard')
        source = es_document['_source']
        d = Dashboard()
        d.id = es_document['_id']
        d.title = source['title']
        d.description = source['description']
        d.hits = source['hits']
        d.panels = cls.unserialize(source['panelsJSON'])
        d.options = cls.unserialize(source['optionsJSON'])
        d.ui_state = cls.unserialize(source['uiStateJSON'])
        d.version = source['version']
        d.time_restore = source['timeRestore']
        d.time_to = source['timeTo']
        d.time_from = source['timeFrom']
        d.refresh_interval_value = source['refreshInterval']['value']
        d.search_source = cls.unserialize(source['kibanaSavedObjectMeta']['searchSourceJSON'])
        return d

    def to_kibana(self):
        return {
            'title': self.title,
            'description': self.description,
            'hits': self.hits,
            'panelsJSON': self.serialize(self.panels),
            'optionsJSON': self.serialize(self.options),
            'uiStateJSON': self.serialize(self.ui_state),
            'version': self.version,
            'timeRestore': self.time_restore,
            'timeTo': self.time_to,
            'timeFrom': self.time_from,
            'refreshInterval': {
                'display': "Off",
                'pause': False,
                'value': self.refresh_interval_value
            },
            'kibanaSavedObjectMeta': {
                'searchSourceJSON': self.serialize(self.search_source)
            }
        }

    def __unicode__(self):
        return self.title


class Dashboards(KibanaApiBase):
    """
    Manages Kibana dashboards
    """
    index = '.kibana'
    doc_type = 'dashboard'

    def get_all(self):
        """
        Returns a list of all dashboards
        :return:
        """
        res = self.es.search(index=self.index, doc_type=self.doc_type, body={'query': {'match_all': {}}})
        if not res['hits']['total']:
            return []
        return [Dashboard.from_kibana(hit) for hit in res['hits']['hits']]

    def add(self, dashboard):
        """
        Created a new dashboard
        :param dashboard: instance of Dashboard
        :return:
        """
        res = self.es.create(index=self.index, id=str(uuid.uuid1()), doc_type=self.doc_type,
                             body=dashboard.to_kibana(), refresh=True)

    def update(self, dashboard):
        """
        Updated the existing dashboard
        :param dashboard: instance of Dashboard that was previously loaded
        :return:
        """
        res = self.es.update(index=self.index, id=dashboard.id, doc_type=self.doc_type,
                             body={'doc': dashboard.to_kibana()},
                             refresh=True)
        return res

    def remove(self, dashboard):
        """
        Deletes the dashboard
        :param dashboard:
        :return:
        """
        res = self.es.delete(index=self.index, id=dashboard.id, doc_type=self.doc_type, refresh=True)
        return res