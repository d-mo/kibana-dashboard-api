from .common import KibanaApiModelBase, KibanaApiBase
import uuid
from functools import reduce
from .paneltools import append_panel


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

    def add_visualization(self, visualization, size_x=6, size_y=3, col=0, row=0):
        """
        Adds the visualization to the dashboard. Leave col and row = 0 for automatic placement of the visualization.
        Visualizations are placed on a grid with 12 columns and unlimited rows.
        :param visualization: previously loaded visualization
        :param size_x width of the panel
        :param size_y height of the panel
        :param col 1-based column of the top left corner, leave 0 for automatic placement
        :param row 1-based row of the top left corner, leave 0 for automatic placement
        :return: newly created panel or None
        """
        new_panel_index = self.get_max_index()+1
        if col and row:
            new_panel = {
                'col': col, 'row': row,
                'size_x': size_x, 'size_y': size_y,
                'panelIndex': new_panel_index,
                'type': 'visualization',
                'id': visualization.id
            }
            self.panels.append(new_panel)
            return new_panel
        else:
            new_panel = append_panel(self.panels, size_x, size_y)
            if new_panel:
                new_panel['id'] = visualization.id
                new_panel['panelIndex'] = new_panel_index
                new_panel['type'] = 'visualization'
                return new_panel

    def remove_visualization(self, visualization_id):
        """
        Removes all visualizations with the specified id from the dashboard
        :param visualization_id:
        :return:
        """
        for i, panel in enumerate(self.panels):
            if panel['id'] == visualization_id:
                del self.panels[i]

    def get_max_index(self):
        return reduce(lambda max_index, panel: max(max_index, panel['panelIndex']), self.panels, 0)


class DashboardsManager(KibanaApiBase):
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
        Creates a new dashboard
        :param dashboard: instance of Dashboard
        :return:
        """
        res = self.es.create(index=self.index, id=str(uuid.uuid1()), doc_type=self.doc_type,
                             body=dashboard.to_kibana(), refresh=True)

    def update(self, dashboard):
        """
        Updates the existing dashboard
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

