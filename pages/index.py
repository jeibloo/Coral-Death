import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import random
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

### APP CALLBACK MUST BE IN BEGINNING BEFORE FUNCTION
@app.callback(
    Output('pButton','n_clicks'),
    [Input(component_id='rButton', component_property='n_clicks')]
)
def update(reset):
    return 0
@app.callback(
    Output(component_id='output-div', component_property='children'),
    [Input(component_id='coral_quantity', component_property='value'),
     Input(component_id='year_choice', component_property='value'),
     Input(component_id='lon', component_property='value'),
     Input(component_id='lat', component_property='value'),
     Input(component_id='region_choice', component_property='value'),
     Input(component_id='pButton', component_property='n_clicks')]
     )
def inputParams(coral, year, lon, lat, region_choice, n_clicks):

    print("\nTEST:\t",type(n_clicks),type(lat),type(lon),
            type(region_choice),type(coral))
    print(n_clicks)

    # To get the callback stuff to stop complaining
    if lon is None or lat is None or coral is None:
        lon = 0
        lat = 0
        coral = 0

    y_pred_list = []
    # Here is when the button is pressed you activate the real part of the function.
    if n_clicks == 1:
        n_clicks = 0
        for i in range(0, coral):
            # Unfortunate extreme fuzzing of an already poor model SORRY FOLKS.
            raw = {'LAT':[random.randint(int(lat)-10,int(lat)+10)],
                   'LON':[random.randint(lon-10,lon+10)],
                   'MONTH':[random.randint(1,13)],'YEAR':[year],
                   'REGION':[region_choice],'SUBREGION':[random.randint(0,255)],
                   'COUNTRY':[random.randint(0,200)],'SOURCE':[random.randint(0,300)]}

            special = pd.DataFrame(raw,columns=list(raw.keys()))
            y_pred_list.append(pipey.predict(special)[0])
        ## Test plain return
        y_pred_list.sort()
        return y_pred_list
    return None

fig = px.scatter_geo(coral,
            lat='LAT',lon='LON',
            color="BLEACHING_SEVERITY",
            projection="orthographic",hover_name='LOCATION',
            animation_frame='YEAR', range_color=(0,4),
            color_continuous_scale=px.colors.diverging.Portland,
            labels={'BLEACHING_SEVERITY':'Level of Bleaching'},
            #center={'lat':9.934739,'lon':-84.087502}, # Unfortunately there may be a bug.
            width=None,height=None).update_layout(
                  autosize=True,height=800,width=1000
                  )

### Leftmost columns
aColumn1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Prediction
            ##### No more shallow coral.

            Coral-Death is an online app that shows the devastating dieout
            of our vital coral reefs. It's purpose is to try and warn what the data
            has shown me, that regardless of where you are any coral reefs near you
            seems likely to perish.
            """
        ),
        # Here we're going to do the prediction stuff.
        html.Div([
            dcc.Markdown("###### Region"),
            dcc.Dropdown(
                id='region_choice',
                options=[{'label':"Asia",'value':'Asia'},
                         {'label':"Australia",'value':'Australia'},
                         {'label':"Pacific",'value':'Pacific'},
                         {'label':"Middle East",'value':'Middle East'},
                         {'label':"Africa",'value':'Africa'},
                         {'label':"Americas",'value':'Americas'}],
            ),
            dcc.Markdown("""
                         ---
                         ###### Coordinates (will not be limited to region)
                         """),
            dbc.Row([
                dcc.Input(id='lat',
                          type='number',
                          placeholder="Latitude\t\t-90  +90",
                          value=''),
                dcc.Input(id='lon',
                          type='number',
                          placeholder="Longitude\t-180 +180",
                          value=''),
            ], className='coord'),
            dcc.Markdown(
            """
            ---
            ###### Amount of Coral
            """),
            dcc.RadioItems(
                id='coral_quantity',
                options=[{'label':'5 Coral','value':5},
                         {'label':'25 Coral','value':25},
                         {'label':'50 Coral','value':50},
                         {'label':'100 Coral','value':100},
                         ],
                labelStyle={'display':'inline-block'},
            ),
            dcc.Markdown(
            """
            ---
            ###### Future
            """),
            dcc.Slider(
                id='year_choice',
                min=2020,
                max=2025,
                value=2020,
                marks={2020:'2020',2021:'2021',
                       2022:'2022',2023:'2023',
                       2024:'2024',2025:'2025'},
                step=10,
            )], className='prediction_werk',
        ),
        html.Div([
            dcc.Markdown(
                """
                *WARNING: bleaching degree is extreme speculation - many other
                features in model are fuzzed for ease-of-use. DO NOT USE for
                real prediction.*
                """
            )
        ],id='warning-div'),
        dbc.Row([
            html.Button('Predict',id='pButton',n_clicks=0),
            html.Button('Reset',id='rButton',n_clicks=0),
        ]),
        html.Div([
        ],id='output-div'),
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

layout = html.Div([
    dbc.Row([bColumn1]),
    dbc.Row([
        dbc.Col(aColumn1,width={'size':5,'offset':1},
        ),
        dbc.Col(aColumn2,width={'size':5,'offset':1})
        ]),
    ]
)
