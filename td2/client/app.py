from dash import dcc,html,Input,Output,State
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc,dash_table
import requests 

lModels = [
            "Decision Tree Classifier",
            "Random Forest",
            "SVC"
        ]

lPenguinsIslands = [
    "Biscoe",
    "Dream",
    "Torgersen"
]

lPenguinsSex = [
    "Male",
    "Female",
]
app = dash.Dash(
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        ["https://codepen.io/chriddyp/pen/bWLwgP.css"],
    ]
)
app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"})
app.config.prevent_initial_callbacks = 'initial_duplicate'
app.config['suppress_callback_exceptions'] = True

sidebar = html.Div(
            [
                html.Div(
                [
                    html.H1("Menu",style={"text-decoration":"underline"}),
                    html.H2(id="menu-pred",children = ["Iris prediction"],className="menu-opt",style={"color":"whitesmoke"}),
                    html.H2(id="menu-fruits",children = ["Fruits menu"],className="menu-opt"),
                ],style={"margin-top": "50%"}
                )
            ]
          ,id="sidebar")
irisDiv = html.Div(
            [
                html.Label(["Sepal Length: ",html.Span(id="curr-sepal-length",children=5)]),
                dcc.Slider(
                    id='sepal-length',
                    min=0,
                    max=10,
                    step=0.1,
                    value=5,
                    marks={i: f'{i:.1f}' for i in range(0, 11, 1)}  # Clean marks with step of 5
                ),

                html.Label(["Sepal Width: ",html.Span(id="curr-sepal-width",children=4)]),
                dcc.Slider(
                    id='sepal-width',
                    min=0,
                    max=8,
                    step=0.1,
                    value=4,
                    marks={i: f'{i:.1f}' for i in range(0, 9, 1)},  # Clean marks with step of 5
                ),

                html.Label(["Petal Length: ",html.Span(id="curr-petal-length",children=4)]),
                dcc.Slider(
                    id='petal-length',
                    min=0,
                    max=8,
                    step=0.1,
                    value=4,
                    marks={i: f'{i:.1f}' for i in range(0, 9, 1)},  # Clean marks with step of 5
                ),

                html.Label(["Petal Width: ",html.Span(id="curr-petal-width",children=2)]),
                dcc.Slider(
                    id='petal-width',
                    min=0,
                    max=4,
                    step=0.1,
                    value=2,
                    marks={i: f'{i:.1f}' for i in range(0, 5, 1)},  # Clean marks with step of 5
                ),

                html.Label("Model :"),
                dcc.Dropdown(
                    id='cb-model',
                    options=[{'label': model_name, 'value': model_name} for model_name in lModels],
                    style={'max-width': '700px', 'margin': 'auto', 'margin-bottom': '15px','width':'100%'}
                )
            ]
        )   

penguinsDiv = html.Div(
            [
                html.Label("Island :"),
                dcc.Dropdown(id='island',options = [{"label":label, "value":label} for label in lPenguinsIslands],style={'width':'100%'}),

                html.Label(["Culmen Length: ",html.Span(id="curr-culmen-length",children=47.5)]),
                dcc.Slider(
                    id='culmen-length',
                    min=25,
                    max=70,
                    step=0.25,
                    value=47.5,
                    marks={i: f'{i:.1f}' for i in range(25, 71, 5)},  # Clean marks with step of 5
                ),

                html.Label(["Culmen Depth: ",html.Span(id="curr-culmen-depth",children=17.5)]),
                dcc.Slider(
                    id='culmen-depth',
                    min=10,
                    max=25,
                    step=0.1,
                    value=17.5,
                    marks={i: f'{i:.1f}' for i in range(10, 26, 1)},  # Clean marks with step of 5
                ),

                html.Label(["Flipper Length: ",html.Span(id="curr-flipper-length",children=200)]),
                dcc.Slider(
                    id='flipper-length',
                    min=160,
                    max=240,
                    step=0.25,
                    value=200,
                    marks={i: f'{i:.1f}' for i in range(160, 241, 5)},  # Clean marks with step of 5
                ),

                html.Label(["Body Mass: ",html.Span(id="curr-body-mass",children=4500)]),
                dcc.Slider(
                    id='body-mass',
                    min=2500,
                    max=6500,
                    step=1,
                    value=4500,
                    marks={i: f'{i:.1f}' for i in range(2500, 6501, 1000)},  # Clean marks with step of 5
                ),

                html.Label("Sex:"),
                dcc.Dropdown(id='sex',options = [{"label":label, "value":label} for label in lPenguinsSex]),

                html.Label("Model :"),
                dcc.Dropdown(
                    id='cb-model',
                    options=[{'label': model_name, 'value': model_name} for model_name in lModels],
                    style={'max-width': '700px', 'margin': 'auto', 'margin-bottom': '15px','width':'100%'}
                )
            ]
        )     
predictionView =  html.Div([
        html.H1(id="lbl-dataset", className="text-center mb-4"),
        dcc.Dropdown(id="cb-dataset",value="iris",options=[{'label': "Iris", 'value': "iris"},{"label":"Penguins","value":"penguins"}],style={'max-width': '700px','margin':'auto','width':'100%'}),
        html.Div(id="prediction-form",children=[
            irisDiv
        ], style={'max-width': '700px', 'margin': 'auto'}),
        html.Div([
            html.Button('Predict', id='btn-predict', className="btn btn-primary mx-auto d-block", style={'width': '100%'})
        ], style={'max-width': '700px','margin':'auto'}),html.Br(),
        html.Div([
            html.Button('Clear inputs', id='btn-clear', className="btn btn-danger mx-auto d-block", style={'width': '100%'})
        ], style={'max-width': '700px','margin':'auto'}),
        html.Div(id='model-accuracy-output-iris', className="lead text-center mt-4"),
        html.Div(id='prediction-output-iris', className="lead text-center mt-4"),
        html.Div(id='model-accuracy-output-penguins', className="lead text-center mt-4"),
        html.Div(id='prediction-output-penguins', className="lead text-center mt-4"),
    ],style={"padding-top":"50px","margin-left":"15%"})

fruitsView = html.Div(id="fruits",children=
                [
                    html.Div([
                        html.H1("Fruits panel", className="text-center mb-4"),
                        html.H3("Insert fruit(s)"),html.Br(),
                        html.Label(id="lbl-output"),
                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id="cb-insert", options=["apple", "mango", "banana", "kiwi", "pear", "papaya"],
                                                multi=True, style={"width": "500px"}), width=8),
                            dbc.Col([
                                dbc.Button(id="btn-insert", children="Insert",className="btn btn-primary",style={"margin-left":"20px"}),
                                dbc.Button(id="btn-flush", children="Flush fruits",className="btn btn-danger",style={"margin-left":"5px"}),
                            ], width=4),
                        ], className="my-3"),
                        html.Div(
                            id="div-dash-table",
                            children=[ 
                                html.H3("Current fruit list"),html.Br(),
                                dash_table.DataTable(id='fruits-table',data=[],style_cell={'textAlign': 'center'})
                            ],style={'padding-top':'40px','width':'100%'}
                        )
                    ],style={'max-width': '700px','margin-left':'35%'})
                ],style={"padding-top":"50px"}
            )          

@app.callback(
    Output('fruits-table','data',allow_duplicate=True),
    Output('lbl-output','children',allow_duplicate=True),
    Output('lbl-output','style',allow_duplicate=True),
    Input('btn-flush','n_clicks'),
    State('fruits-table','data'),
) 
def flushFruits(n_clicks,fruits):
    if n_clicks:
        response = requests.delete("http://fruits_api:5002/flush/fruits")
        if response:
            return [],"SUCCESS : All fruits have been successfully flushed !",{"color":"green"}
        else:
            return fruits,"ERROR : Couldn't flush fruits collection",{"color":"red"}            


@app.callback(
    Output('cb-insert','value'),
    Output('fruits-table','data',allow_duplicate=True),
    Output('lbl-output','children'),
    Output('lbl-output','style'),
    Input('btn-insert','n_clicks'),
    State('cb-insert','value')
)
def insertFruit(n_clicks,selectedFruits):
    response = requests.get("http://fruits_api:5002/fruits")
    if n_clicks:
        if not(selectedFruits):
            return "",response.json()["fruits"],"ERROR : You need to select a fruit at least",{"color":"red"} 
        headers = {'Content-Type': 'application/json'}
        response = requests.post("http://fruits_api:5002/add/fruit",headers=headers,json={"fruits":selectedFruits})
        lblOutputColor = "green" if response.json()[0] else "red"
        lbltextOutput = "SUCCESS: Fruit added successfully !" if response.json()[0] else "ERROR: fruit insertion failed"
        return "",response.json()[1],lbltextOutput,{"color":lblOutputColor}
    return "",response.json()["fruits"],"",{}

@app.callback(
    Output('lbl-dataset','children',allow_duplicate=True),
    Output('prediction-form','children',allow_duplicate=True),
    Output('model-accuracy-output-iris','children',allow_duplicate=True),
    Output('prediction-output-iris','children',allow_duplicate=True),
    Output('model-accuracy-output-penguins','children',allow_duplicate=True),
    Output('prediction-output-penguins','children',allow_duplicate=True),
    Input('cb-dataset','value')
)
def displayDatasetControls(dataset):
    if dataset:
        stringVar = f"{dataset}Div"
        divVar = globals().get(stringVar, f"No content for {stringVar}")
        return f"{dataset.capitalize()} species prediction",divVar,[],[],[],[]

        
@app.callback(
    Output('model-accuracy-output-iris','children',allow_duplicate=True),
    Output('prediction-output-iris','children',allow_duplicate=True),
    Input('btn-predict','n_clicks'),
    State('cb-dataset','value'),
    State('sepal-length','value'),
    State('sepal-width','value'),
    State('petal-length','value'),
    State('petal-width','value'),
    State('cb-model','value'),
)
def predictIris(n_clicks,dataset,sepal_length,sepal_width,petal_length,petal_width,model):
    if n_clicks:
        if dataset=="iris":
            if not(sepal_length) or not(sepal_width) or not(petal_length) or not(petal_width) or not(model):
                return "You need to fill in every inputs",""
            params = {
                'sepal_length': sepal_length,
                'sepal_width': sepal_width,
                'petal_length': petal_length,
                'petal_width': petal_width,
                'model_name': model
            }
            response = requests.get("http://predictions_api:5001/predict/iris",params=params)
            data = response.json()      

            return data[0],data[1]
        
@app.callback(
    Output('curr-sepal-length','children'),
    Input("sepal-length","value")
)
def showCurrentSepalLength(value):
    if value:
        return value

@app.callback(
    Output('curr-sepal-width','children'),
    Input("sepal-width","value")
)
def showCurrentSepalWidth(value):
    if value:
        return value

@app.callback(
    Output('curr-petal-length','children'),
    Input("petal-length","value")
)
def showCurrentPetalLength(value):
    if value:
        return value

@app.callback(
    Output('curr-petal-width','children'),
    Input("petal-width","value")
)
def showCurrentPetalWidth(value):
    if value:
        return value


@app.callback(
    Output('model-accuracy-output-penguins','children',allow_duplicate=True),
    Output('prediction-output-penguins','children',allow_duplicate=True),
    Input('btn-predict','n_clicks'),
    State('cb-dataset','value'),
    State('island','value'),
    State('culmen-length','value'),
    State('culmen-depth','value'),
    State('flipper-length','value'),
    State('body-mass','value'),
    State('sex','value'),
    State('cb-model','value'),
)
def predictPenguins(n_clicks,dataset,island,culmen_length,culmen_depth,flipper_length,body_mass,sex,model):
    if n_clicks:
        if dataset=="penguins":
            if not(island) or not(culmen_length) or not(culmen_depth) or not(flipper_length) or not(body_mass) or not(sex) or not(model):
                return "You need to fill in every inputs",""
            params = {
                'island': island,
                'bill_length': culmen_length,
                'bill_depth': culmen_depth,
                'flipper_length': flipper_length,
                'body_mass': body_mass,
                'sex': sex,
                'model_name': model
            }
            response = requests.get("http://predictions_api:5001/predict/penguins",params=params)
            data = response.json()      

            return data[0],data[1]

@app.callback(
    Output('curr-culmen-length','children'),
    Input("culmen-length","value")
)
def showCurrentCulmenLength(value):
    if value:
        return value

@app.callback(
    Output('curr-culmen-depth','children'),
    Input("culmen-depth","value")
)
def showCurrentCulmenDepth(value):
    if value:
        return value

@app.callback(
    Output('curr-flipper-length','children'),
    Input("flipper-length","value")
)
def showCurrentFlipperLength(value):
    if value:
        return value

@app.callback(
    Output('curr-flipper-depth','children'),
    Input("culmen-depth","value")
)
def showCurrentCulmenDepth(value):
    if value:
        return value

@app.callback(
    Output('curr-body-mass','children'),
    Input("body-mass","value")
)
def showCurrentBodyMass(value):
    if value:
        return value
    
@app.callback(
    Output('model-accuracy-output-iris','children',allow_duplicate=True),
    Output('prediction-output-iris','children',allow_duplicate=True),
    Output('sepal-length','value'),
    Output('sepal-width','value'),
    Output('petal-length','value'),
    Output('petal-width','value'),
    Input('btn-clear','n_clicks'),
    State('sepal-length','value'),
    State('sepal-width','value'),
    State('petal-length','value'),
    State('petal-width','value'),
    State('model-accuracy-output-iris','children'),
    State('prediction-output-iris','children'),
    State('cb-dataset','value'),
    prevent_initial_callback = True
)
def clearInputsIris(n_clicks,sepal_length,sepal_width,petal_length,petal_width,model_accuracy,prediction,dataset):
    if n_clicks:
        if dataset=="iris": 
            return [],[],5,4,4,2
    return model_accuracy,prediction,sepal_length,sepal_width,petal_length,petal_width

@app.callback(
    Output('model-accuracy-output-penguins','children',allow_duplicate=True),
    Output('prediction-output-penguins','children',allow_duplicate=True),
    Output('island','value'),
    Output('culmen-length','value'),
    Output('culmen-depth','value'),
    Output('flipper-length','value'),
    Output('body-mass','value'),
    Output('sex','value'),
    Input('btn-clear','n_clicks'),
    State('island','value'),
    State('culmen-length','value'),
    State('culmen-depth','value'),
    State('flipper-length','value'),
    State('body-mass','value'),
    State('sex','value'),
    State('model-accuracy-output-penguins','children'),
    State('prediction-output-penguins','children'),
    State('cb-dataset','value'),
    prevent_initial_callback = True
)
def clearInputsPenguins(n_clicks,island,culmen_length,culmen_depth,flipper_length,body_mass,sex,model_accuracy,prediction,dataset):
    if n_clicks:
        if dataset=="penguins": 
            return [],[],"",47.5,17.5,200,4500,""
    return model_accuracy,prediction,island,culmen_length,culmen_depth,flipper_length,body_mass,sex


@app.callback(
    Output('menu-pred','style',allow_duplicate=True),
    Output('menu-fruits','style',allow_duplicate=True),
    Output('div-main','children',allow_duplicate=True),
    Input('menu-pred','n_clicks')
)
def displayFruits(n_clicks):
    if n_clicks:
        return {"color":"white"},{"color":"black"},predictionView
    return {},{},fruitsView

@app.callback(
    Output('menu-fruits','style',allow_duplicate=True),
    Output('menu-pred','style',allow_duplicate=True),
    Output('div-main','children',allow_duplicate=True),
    Input('menu-fruits','n_clicks')
)
def displayFruits(n_clicks):
    if n_clicks:
        return {"color":"white"},{"color":"black"},fruitsView
    return {},{},predictionView

main = html.Div([sidebar,html.Div(id="div-main",children=predictionView)])

app.layout = main

if __name__ == "__main__":
    app.run_server(host='0.0.0.0')