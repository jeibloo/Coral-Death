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
            color_continuous_scale=px.colors.diverging.Portland,
            projection="natural earth",
            width=None,height=None)

'''
#### BEGINNING OF REAL
@app.callback(
    Output('prediction-content','children'),
    [Input('COUNTRY','value'), Input('YEAR','value')])
def predict(COUNTRY, YEAR):
    df = pd.DataFrame(
        columns=['COUNTRY','YEAR'],
        data = [[YEAR,COUNTRY]]
    )
    y_pred = pipey.predict(df)[0]
    return f'{y_pred:.0f} bleached?'
#### END OF REAL
'''
#### BEGINNING OF TEST
### APP CALLBACK MUST BE IN BEGINNING BEFORE FUNCTION
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')])
def inputTest(input_value):
    return '{}'.format(input_value)
#### END OF TEST

fig = px.scatter_geo(coral,
            lat='LAT',lon='LON',
            color="BLEACHING_SEVERITY",
            projection="orthographic",hover_name='LOCATION',
            animation_frame='YEAR', range_color=(0,4),
            color_continuous_scale=px.colors.diverging.Portland,
            labels={'BLEACHING_SEVERITY':'Level of Bleaching'},
            #center={'lat':9.934739,'lon':-84.087502}, # Unfortunately this doesn't work right
            width=None,height=None).update_layout(
                  autosize=True,height=800,width=1000
                  )

### Leftmost columns
aColumn1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Predictions
            ##### No more shallow coral.

            Coral-Death is an online app that shows the devastating dieout
            of our vital coral reefs. It's purpose is to try and warn what the data
            has shown me, that regardless of where you are any coral reefs near you
            seems likely to perish.
            """
        ),
        # Here we're going to do the prediction stuff.
        html.Div([
            dcc.Input(id='my-id', value='', type='text'),
            dcc.Slider(
                id='YEAR',
                min=2013,
                max=2100,
                step=5,
                value=2013),
            ], className='jumanji',
        ),
        html.Div([

        ],id='my-div')
    ],
    md=10,
)

### Rightmost column
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

            After much thought my original plan of detecting if a coral group
            was bleaching or not was not going to work. The reason being that since
            the data was so overwhelming in favour of almost all of the coral dying,
            my ROC AUC scores were very close to perfect the entire time.
            Only when I would train my data starting from the early 90's and back
            is when the Predictions became a hair less than perfect.

            I was aware of the fact the coral was being recorded could be a sign of bleaching
            (since the contrast between the bright alive coral and white and lifeless kind would
            be easy to spot before most knew about this great bleaching) therefore skewing my earlier decade data.
            But putting that aside, my model seemed to see an obvious trend
            in this specific dataset that says that the coral is bleaching,
            and will continue to bleach until proabably most of the shallow water coral that
            is non-resistant to heat is dead.

            """
        ),
        dcc.Link(dbc.Button('Learn More about the Process', color='secondary'), href='/process')
    ],
    md=10,
)

### Even though it says bColumn it's the big globe on top. lol
bColumn1 = dbc.Col(
    [
        dcc.Graph(figure=fig),
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
    ]
)
