


from plotly import tools
tools.set_credentials_file(username='hick', api_key='phFKCu1UETF03TXbu4Ni')


import plotly.plotly as py
import plotly.graph_objs as go
from IPython.display import Image
from plotly.widgets import GraphWidget



url = py.plot({'data': [go.Scatter(x=[1, 2, 3], y=[4, 6, 9]), go.Scatter(x=[1, 2, 3], y=[10, 30, 20])]},
               filename = 'widget template', auto_open=False)
print(url)

graph = GraphWidget(url)
g = graph
graph