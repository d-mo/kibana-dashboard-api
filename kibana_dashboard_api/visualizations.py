from .common import KibanaApiBase, KibanaApiModelBase
import uuid


class Visualization(KibanaApiModelBase):
    """
    Visualization model
    """
    id = None
    title = None
    description = None
    vis_state = None
    ui_state = None
    search_source = None

    @classmethod
    def from_kibana(cls, es_document):
        if es_document.get('_type') != 'visualization':
            raise Exception('The document is not visualization')
        source = es_document['_source']
        v = Visualization()
        v.id = es_document['_id']
        v.title = source['title']
        v.description = source['description']
        v.ui_state = source['uiStateJSON']
        v.vis_state = cls.unserialize(source['visState'])
        v.search_source = cls.unserialize(source['kibanaSavedObjectMeta']['searchSourceJSON'])
        return v

    def to_kibana(self):
        return {
            'title': self.title,
            'description': self.description,
            'visState': self.serialize(self.vis_state),
            'uiStateJSON': self.ui_state,
            'kibanaSavedObjectMeta': {
                'searchSourceJSON': self.serialize(self.search_source)
            }
        }

    def __str__(self):
        return self.title

    def url_path(self):
        return "/app/kibana#/visualize/edit/{id}?embed=true&_g=(refreshInterval%3A(display%3AOff%2Cpause%3A!f%2Cvalue%3A0)%2Ctime%3A(from%3Anow-7d%2Cmode%3Aquick%2Cto%3Anow))".format(
            id=self.id)


class VisualizationsManager(KibanaApiBase):
    """
    Manages Kibana visualizations
    """
    index = '.kibana'
    doc_type = 'visualization'

    def get_all(self):
        """
        Returns a list of all visualizations
        :return: list of the Visualization instances
        """
        res = self.es.search(index=self.index, doc_type=self.doc_type, body={'query': {'match_all': {}}})
        if not res['hits']['total']:
            return []
        return [Visualization.from_kibana(hit) for hit in res['hits']['hits']]

    def add(self, visualization):
        """
        Creates a new visualization
        :param visualization: instance of Visualization
        :return:
        """
        res = self.es.create(index=self.index, id=str(uuid.uuid1()), doc_type=self.doc_type,
                             body=visualization.to_kibana(), refresh=True)
        return res

    def update(self, visualization):
        """
        Updates existing visualization
        :param visualization: instance of Visualization that was previously loaded
        :return:
        """
        res = self.es.update(index=self.index, id=visualization.id, doc_type=self.doc_type,
                             body={'doc': visualization.to_kibana()},
                             refresh=True)
        return res

    def remove(self, visualization):
        """
        Deletes the visualization
        :param visualization: instance of Visualization that was previously loaded
        :return:
        """
        res = self.es.delete(index=self.index, id=visualization.id, doc_type=self.doc_type, refresh=True)
        return res


class VisualizationTemplatesManager(VisualizationsManager):
    """
    Manages visualization templates. Creates a new document type vis_template in the Kibana index
    """
    index = '.kibana'
    doc_type = 'vis_template'