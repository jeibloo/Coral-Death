import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

Layout in Bootstrap is controlled using the grid system. The Bootstrap grid has
twelve columns.

There are three main layout components in dash-bootstrap-components: Container,
Row, and Col.

The layout of your app should be built as a series of rows of columns.

We set md=4 indicating that on a 'medium' sized or larger screen each column
should take up a third of the width. Since we don't specify behaviour on
smaller size screens Bootstrap will allow the rows to wrap so as not to squash
the content.
"""

aColumn1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Why do they die?

            THIS APP SHALLE BENEFIT U. Don't emphasize the underlying technology.

            ✅ RUN is a running app that adapts to your fitness levels and designs personalized workouts to help you improve your running.

            ❌ RUN is the only intelligent running app that uses sophisticated deep neural net machine learning to make your run smarter because we believe in ML driven workouts.

            """
        ),
        dcc.Link(dbc.Button('Call To Action', color='primary'), href='/predictions')
    ],
    md=10,
)
aColumn2 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Does this thing Run DOOM?

            THIS APP SHALLE BENEFIT THU. Don't emphasize the underlying technology.

            If you think you know, now you know.

            """
        ),
    ],
    md=10,
)

### Here is the data 3D cool thing
gapminder = px.data.gapminder()
fig = px.line_geo(gapminder.query("year==2007"),
                  locations="iso_alpha", color="continent",
                  projection="orthographic",
                  width=None,height=None).update_layout(
                  autosize=True,height=1000,width=1000
                  )

bColumn1 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ],
)

layout = html.Div([
    dbc.Row([bColumn1]),
    dbc.Row([
        dbc.Col(aColumn1,width={'size':5,'offset':1}),
        dbc.Col(aColumn2,width={'size':5,'offset':1})
        ])
    ]
)
