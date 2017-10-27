# kibana-dashboard-api
List/create/delete Kibana visualizations and dashboards directly manipulating Elasticsearch index.

[![Build Status](https://travis-ci.org/harabchuk/kibana-dashboard-api.svg?branch=master)](https://travis-ci.org/harabchuk/kibana-dashboard-api)

## Intro

### Visualizations

```python
from kibana_dashboard_api import VisualizationsManager, DashboardsManager
from elasticsearch import Elasticsearch

es_connection = Elasticsearch(hosts=['http://login:pass@localhost:9200/'])

visualizations = VisualizationsManager(es_connection)

# list all visualizations
vis_list = visualizations.get_all()
for vis in vis_list:
    print(vis.title)


#change the title of the first visualization and save it
vis = vis_list[0]
vis.title = 'New Title'
visualizations.update(vis)

```

### Dashboards

```python
dashboards = DashboardsManager(es_connection)

# list all dashboards
dash_list = dashboards.get_all()
for d in dash_list:
    print(d.title)

# Add a visualization to the first dashboard
dash = dash_list[0]
dash.add_visualization(vis, 6, 3)
dashboards.update(dash)
```

## Installation

``` 
pip install kibana-dashboard-api
```


