import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Process
            ### Note: this process is for the strange binary classification attempt.
            ### For the multi-class one it's similar.
            ---

            #### Import, Cutting, Wranglin'

            First I imported the excel file from Reefbase. Then I set the target
            and switched all the known bleachings to 1 and the unknown bleachings
            to zero.

            ```
            import pandas as pd
            df = pd.read_excel('./dataset/CoralBleaching.xlsm')
            target = 'BLEACHING_SEVERITY'
            ```
            When I looked up what `Severity Unknown` was in the relevant documentation
            I discovered that in fact those reefs *were* bleached, they just didn't
            know how severe.

            Also had one value: Latitude->-10269 (which is an impossible number for
            latitude) to convert manually.

            ```
            def wgle(df):
                # Group by bleaching or not
                df[target] = df[target].replace({
                    'Low':1, 'HIGH':1, 'Medium':1, 'Severity Unknown':1,
                    'No Bleaching':0})

                # Get all features for ease-of-use
                features, num_feats, cat_feats = bc.pantryFeatures(df)

                # Drop columns with almost no values.
                df = bc.diceUglyCols(df, features, percent=50)

                # Drop severity code cause that's obviously a leakage
                df = df.drop('SEVERITY_CODE',axis=1)

                # Special weird values
                df['LAT'] = df['LAT'].replace({-10269:-10.269})

                return df
            ```

            Then I wrangled the data as per the function up there and got a
            `df.profile_report()` of the newly cleaned dataframe.
            """),
        html.Img(src='assets/heatmap_wrangled.png',className='img-fluid'),
        dcc.Markdown(
            """
            A few correlations between for example `MONTH` and `BLEACHING_SEVERITY`.

            (I also made sure during many steps to make sure I kept track of how
            many columns I was cutting or manipulating. I also cut `BLEACHING_SEVERITY`
            of course since that would leak if it was bleached or not.)

            ```
            print("Cut down {} columns.".format(df.shape[1]-df_wrangle.shape[1]))
            ```
            The longitudes and latitudes now look appropriate, and it matches up
            with intuition that the majority of the reefs lie between the graphs'
            areas.
            """),
        html.Img(src='assets/longLat.png',className='img-fluid'),
        dcc.Markdown(
            """
            ---
            #### Splitting data

            Decided to split the data by year so had to do so manually.

            ```
            # Split into Train Test & Val by year. Why I didn't use TimeSeriesSplit
            # the world may never know.
            test_mask = (df['YEAR'] > 1999)
            vali_mask = ((df['YEAR'] > 1996) & (df['YEAR'] <= 1999))
            trin_mask = (df['YEAR'] <= 1995)
            # Use masks
            test = df[test_mask].copy()
            trin = df[trin_mask].copy()
            vali = df[vali_mask].copy()
            ```

            Another assurance check to make sure all was well. Then I chopped
            up the sets to isolate the targets and the features I wanted.

            ```
            ### Chop the sets up
            features, _, _ = bc.pantryFeatures(trin)
            X_train = trin[features].drop(target,axis=1)
            y_train = trin[target]

            X_test = test[features].drop(target,axis=1)
            y_test = test[target]

            X_vali = vali[features].drop(target,axis=1)
            y_vali = vali[target]
            ```
            ---
            #### Majority Class Baseline
            Classification problems call for classification metrics.
            ```
            # Majority Class Baseline for just if the coral is bleached or not.
            bc.soupBaseModel(df, target, 1)
            ```
            And it gave me 76.1389% for bleached; 23.8611% for not-bleached.
            ```
            # Majority Class Baseline for the degree of bleaching for Coral.
            bc.soupBaseModel(df, target, 1)
            ```
            Zero is no bleaching, four is worst.

            0: 23.8611%

            1: 19.4023%

            2: 23.0856%

            3: 14.7173%

            4: 18.9338%

            Not looking good for the world of coral.

            ---
            #### Fitting and Predicting
            Made a pipeline to streamline
            ```
            pipey = make_pipeline(
                # Encode values ordinally
                ce.OrdinalEncoder(),
                # Impute NaNs
                SimpleImputer(),
                RandomForestClassifier(
                    n_estimators=500,
                    class_weight='balanced',
                    n_jobs=-1,
                    random_state=4
                )
            )
            ```
            Then I use this pipeline to fit on the training set.
            ```
            pipey.fit(X_train, y_train);
            ```
            Using cross-validation I see how good of an accuracy I can get.
            ```
            cross_val_score(pipey, X_train, y_train, cv=20, scoring='accuracy')
            ```
            The highest I got was 61%.

            ---
            #### Examining the Data

            If I take a look at a partial dependence plot of a single feature in
            isolation (latitude), I can see that there was an effect on the
            outcome.
            """
        ),
        html.Img(src='assets/pdp_lat.png',className='img-fluid'),
        dcc.Markdown(
            """
            And for a Shapley Value Force plot for three interesting individual outcomes.
            """
        ),
        html.Img(src='assets/shapley0.png',className='img-fluid'),
        html.Img(src='assets/shapley1.png',className='img-fluid'),
        html.Img(src='assets/shapley2.png',className='img-fluid'),
        dcc.Markdown(
            """
            ---
            Interestingly enough, for almost every outcome the only major determining
            factor seemed to be the longitude and latitude (with a few caveats for
            country and sometimes source).

            *Unfortunately* I think
            this might mean that the majority of the predictive power comes from outside
            of our dataset. If I were to posit where I could find it, I believe that
            the general heat content of the ocean would be the biggest indicator. But
            all-in-all this was a interesting experiment to see what I could find out.

            As for the multi-class stuff, the process was pretty samey but with the added
            bonus of having a few more options for correctness. This whole dataset winded
            up being very difficult in regards to its lack of data but it was a good
            exercise to see what I could wring out.

            """
        ),

    ],
)

layout = dbc.Row([column1])
