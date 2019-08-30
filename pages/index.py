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
import plotly.graph_objs as go
from collections import Counter
from app import app

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
    Output(component_id='output-graph', component_property='figure'), # Shelve graph for now
    #[Output(component_id='output-x', component_property='children'), # For text
    #Output(component_id='output-y', component_property='children')], # For text
    [Input(component_id='coral_quantity', component_property='value'),
     Input(component_id='year_choice', component_property='value'),
     Input(component_id='lon', component_property='value'),
     Input(component_id='lat', component_property='value'),
     Input(component_id='region_choice', component_property='value'),
     Input(component_id='pButton', component_property='n_clicks')]
     )
def inputParams(coral, year, lon, lat, region_choice, n_clicks):

    # To get the callback stuff to stop complaining
    if lon is None or lat is None or coral is None or region_choice is None:
        lon = 0
        lat = 0
        coral = 0
        region_choice = 0
    # DON'T BE SNEAKY !!!
    elif not isinstance(lon, int):
        lon = 0
    elif not isinstance(lat, int):
        lat = 0
    elif (lon <= -200 or lon >= 200) or (lat <= -200 or lat <= 200):
         lon = 0
         lat = 0

    y_pred_list = []
    # Here is when the button is pressed you activate the real part of the function.
    if n_clicks == 1:
        n_clicks = 0
        wait_dot = ''
        for i in range(0, coral):
            # Unfortunate extreme fuzzing of an already poor model SORRY FOLKS.
            raw = {'LAT':[random.randint(int(lat)-10,int(lat)+10)],
                   'LON':[random.randint(lon-10,lon+10)],
                   'MONTH':[random.randint(1,13)],'YEAR':[year],
                   'REGION':[region_choice],'SUBREGION':[random.randint(0,255)],
                   'COUNTRY':[random.randint(0,200)],'SOURCE':[random.randint(0,300)]}

            ### Make the data frame to predict, I'm so sorry for making a new df each time...
            special = pd.DataFrame(raw,columns=list(raw.keys()))
            y_pred_list.append(pipey.predict(special)[0])
            wait_dot+='.'
            print(wait_dot)
        ### Test plain return
        y_pred_list.sort()
        keyz = list(Counter(y_pred_list).keys())
        valz = list(Counter(y_pred_list).values())
        #return '{} | Bleaching Level'.format(keyz),'\n{} | Quantity'.format(valz)
        return {
            'data': [{
                'type': 'bar',
                'x': keyz,
                'y': valz
            }],
            'layout': {
                'title': 'Bleaching'
            }
        }

    #return '{} | Bleaching Level'.format('NEEDS INPUT'),'\n{} | Quantity'.format('NEEDS INPUT')
    return {
        'data': [{
            'type': 'bar',
            'x': [0,1,2,3,4],
            'y': [0]
        }],
        'layout': {
            'title': 'Bleaching'
        }
    }

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

            Coral-Death is an persistent speculation app that shows the devastating die-out
            of our vital coral reefs. It's purpose is to try to educate as much
            as possible with known historical coral data and show where the coral reefs
            might be five years.
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
        ### Here's output, but god it's so hard to figure out.
        html.Div([
            # nathin'
            # Just the text
            html.P([
            ], id='output-x'),
            html.P([
            ], id='output-y'),
            dcc.Graph(
                id='output-graph',
            )
        ],id='output-div')
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

            When discovering this dataset I outlined a few questions to myself,
            and the answers were not clear cut. The dataset did
            not have good values for water temperature near the affected
            reefs, nor did it have important information such as the recovery of
            the reef in question since the last checkup.

            My original plan of detecting if a coral group was bleaching or not
            was not going to work. Why? Because no matter how I twisted and juggled the
            data my predictive model almost always came out with every coral being bleached
            (up/downsampling was an option and did give me semi-normal results).
            My scores (AUC ROC) were close to perfect the entire time, and it felt like
            there was nothing to predict because the outcome was so inevitable as time passed
            that the model would be *really* useless.
            Only when I would train my data starting from the early 90's and back
            is when the predictions became a hair less than perfect - 99.8% instead of 99.99%.
            I decided to up the granularity and predict the level of bleaching instead,
            but unfortunately my data was lacking *something*. I believe that that *something* may very
            well be the lack of temperature data. Therefore, I was at a loss of any real
            predictive power again.

            As for blind spots: as always, the data can be skewed in some way, especially for
            pre-90s data. (since the contrast between the bright alive coral and white and lifeless kind would
            be easy to spot before most knew about this great bleaching and not many
            seemed to have an inclination towards recording coral health pre-90s).

            ---

            As for secrets, from some of the geospatial graphing (look towards the Great Barrier Reef)
            it seemed that some of the coral that registered a max bleaching (4) in the 90's would
            then later be completely missing in the 2000's. I never got a clear answer to
            this but since other coral further from the coast and around some of those spots
            would go from a 1-3 in the 90's to a 4...worst case scenario is those
            reefs *may* be just completely dead and not worth recording.
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
