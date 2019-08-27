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

            ## Predictions
            ##### The coral is getting bleached

            Coral-Death is an online app that shows the devasting certainty of the death
            of our vital coral reefs to try and spurn action halt climate change.
            Coral-Death is an online app that shows the devasting certainty of the death
            of our vital coral reefs to try and spurn action halt climate change.
            Coral-Death is an onl

            ine app that shows the devasting certainty of the death
            of our vital coral reefs to try and spurn action halt climate change.
            Coral-Death is an online app that shows the devasting certainty of the death
            of our vital coral reefs to try and spurn action halt climate change.
            Coral-Death is an online app that shows the devasting certainty of the death
            of our vital coral reefs to try and spurn action halt climate change.
            Coral-Death is an online app that shows the devasting certainty of the death
            of our vital coral reefs to try and spurn action halt climate change.
            """
        )
    ],
    md=10,
)
aColumn2 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Insights
            ##### Why do they die?
            *Does this thing also run DOOM?*

            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.

            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.
            If you think you know, now you know.

            """
        ),
        dcc.Link(dbc.Button('Learn More about the Process', color='secondary'), href='/process')
    ],
    md=10,
)

### Here is the data 3D cool thing
gapminder = px.data.gapminder()
fig = px.line_geo(gapminder.query("year==2007"),
                  locations="iso_alpha", color="continent",
                  projection="orthographic",
                  width=None,height=None).update_layout(
                  autosize=True,height=800,width=1000
                  )

bColumn1 = dbc.Col(
    [
        dcc.Graph(figure=fig),
        html.Div(
        dcc.Slider(
            id="year",
            min=1969,
            max=2050,
            step=1,
            value=1999,
            className='mb-10',
            updatemode='drag',
        ),id='slider-output-container')
    ],
)

@app.callback(
    dash.dependencies.Output('year', 'children'),
    [dash.dependencies.Input('year', 'value')])
def update_output(value):
    return html.Div("{}".format(value), id='output-text')

layout = html.Div([
    dbc.Row([bColumn1]),
    dbc.Row([
        dbc.Col(aColumn1,width={'size':5,'offset':1}),
        dbc.Col(aColumn2,width={'size':5,'offset':1})
        ])
    ]
)
