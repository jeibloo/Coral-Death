import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
# Get pipey!
from joblib import load
pipey = load('assets/pipey.joblib')

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

### Here is the data 3D cool thing
#coral = pd.read_csv("../notebooks/dataset/CoralBleachingClean.csv",index_col='ID')
coral = pd.read_csv("./CoralBleachingClean.csv",index_col='ID')

figbot = px.scatter_geo(coral,
            lat='LAT',lon='LON',
            color="BLEACHING_SEVERITY",
            color_continuous_scale=px.colors.sequential.Jet,
            projection="natural earth",
            width=None,height=None)

@app.callback(
    Output('prediction-content','children'),
    [Input('COUNTRY','value'), Input('YEAR','value')]
)
def predict(COUNTRY, YEAR):
    df = pd.DataFrame(
        columns=['COUNTRY','YEAR'],
        data = [[YEAR,COUNTRY]]
    )
    y_pred = pipey.predict(df)[0]
    return f'{y_pred:.0f} bleached?'

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
            """
        ),
    ],
    md=10,
)

xColumn1 = dbc.Col(
    [
        dcc.Markdown(
            """
            ### TEST
            """
        ),
    ]
)
aColumn2 = dbc.Col(
    [
        dcc.Markdown(
            """
            ## Insights
            ##### What was unusual? Secrets in the data?

            When first discovering this dataset I'd assumed the answer to many
            of my questions would not be clear cut. After all the dataset did
            not have good values for water temperature near the affected
            reefs, nor did it have important information such as the recovery of
            the reef in question since the last checkup. But nontheless I had chosen
            a dataset and intended to stick with it.

            The answers are still not entirely clear, even with extensive outside
            research. But what I do know is, when trying to train and model my data
            I was getting extremely high scores all the time, and only when I would
            train my data starting from the early 90's and back is when the Predictions
            became a hair less than perfect. Of course the very fact that the coral reefs
            were and are generally being recorded is the obvious signs of bleaching,
            white and brittle, lifeless coral - this is easy to spot.
            But putting that aside, my model seemed to see an obvious trend
            in this specific dataset that says that the coral is bleaching,
            and will continue to bleach until proabably most of the shallow water coral that
            is non-resistant to heat is plain dead.
            """
        ),
        dcc.Link(dbc.Button('Learn More about the Process', color='secondary'), href='/process')
    ],
    md=10,
)

fig = px.scatter_geo(coral,
            lat='LAT',lon='LON',
            color="BLEACHING_SEVERITY",
            projection="orthographic",hover_name='LOCATION',
            animation_frame='YEAR', range_color=(0,1),
            color_continuous_scale=px.colors.diverging.Portland,
            labels={'BLEACHING_SEVERITY':'Currently Bleaching or Not'},
            width=None,height=None).update_layout(
                  autosize=True,height=800,width=1000
                  )

bColumn1 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ],
)

cColumn1 = dbc.Col(
    [
        dcc.Slider(
            id='YEAR',
            min=2013,
            max=2100,
            step=5,
            value=2013
        ),
        dcc.Graph(id='SmallWorld',figure=figbot),
    ],
)

"""
html.Div(
    dcc.Slider(
    id="year",
    min=1952,
    max=2002,
    step=5,
    value=1952,
    className='mb-10',
    updatemode='drag',
),id='slider-output-container')
"""
"""
@app.callback(
    dash.dependencies.Output('year', 'children'),
    [dash.dependencies.Input('year', 'value')])
def update_output(value):
    return html.Div("{}".format(value), id='output-text')
    """

layout = html.Div([
    dbc.Row([bColumn1]),
    dbc.Row([
        dbc.Col(aColumn1,width={'size':5,'offset':1},
        ),
        dbc.Col(aColumn2,width={'size':5,'offset':1})
        ]),
    dbc.Row([cColumn1]),
    ]
)
