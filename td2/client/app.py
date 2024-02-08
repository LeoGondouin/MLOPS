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
                html.Label("Sepal Length:"),
                dbc.Input(id='sepal-length', type='number',className="form-control mb-2"),

                html.Label("Sepal Width:"),
                dcc.Input(id='sepal-width', type='number', className="form-control mb-2"),

                html.Label("Petal Length:"),
                dcc.Input(id='petal-length', type='number', className="form-control mb-2"),

                html.Label("Petal Width:"),
                dcc.Input(id='petal-width', type='number', className="form-control mb-3"),

                html.Label("Model :"),
                dcc.Dropdown(
                    id='cb-model',
                    options=[{'label': model_name, 'value': model_name} for model_name in lModels],
                    style={'max-width': '400px', 'margin': 'auto', 'margin-bottom': '15px'}
                )
            ]
        )   

penguinsDiv = html.Div(
            [
                html.Label("Island :"),
                dcc.Dropdown(id='island',options = [{"label":label, "value":label} for label in lPenguinsIslands]),

                html.Label("Culmen Length:"),
                dcc.Input(id='culmen-length', type='number', className="form-control mb-2"),

                html.Label("Culmen Depth:"),
                dcc.Input(id='culmen-depth', type='number', className="form-control mb-2"),

                html.Label("Flipper Length:"),
                dcc.Input(id='flipper-length', type='number', className="form-control mb-2"),

                html.Label("Body Mass:"),
                dcc.Input(id='body-mass', type='number', className="form-control mb-3"),

                html.Label("Sex:"),
                dcc.Dropdown(id='sex',options = [{"label":label, "value":label} for label in lPenguinsSex]),

                html.Label("Model :"),
                dcc.Dropdown(
                    id='cb-model',
                    options=[{'label': model_name, 'value': model_name} for model_name in lModels],
                    style={'max-width': '400px', 'margin': 'auto', 'margin-bottom': '15px'}
                )
            ]
        )     
predictionView =  html.Div([
        html.H1(id="lbl-dataset",children="Iris Species Prediction", className="text-center mb-4"),
        dcc.Dropdown(id="cb-dataset",value="iris",options=[{'label': "Iris", 'value': "iris"},{"label":"Penguins","value":"penguins"}],style={'max-width': '400px','margin':'auto'}),
        html.Div(id="prediction-form",children=[
            irisDiv
        ], style={'max-width': '400px', 'margin': 'auto'}),
        html.Div([
            html.Button('Predict', id='btn-predict', className="btn btn-primary mx-auto d-block", style={'width': '100%'})
        ], style={'max-width': '400px','margin':'auto'}),html.Br(),
        html.Div([
            html.Button('Clear inputs', id='btn-clear', className="btn btn-primary mx-auto d-block", style={'width': '100%'})
        ], style={'max-width': '400px','margin':'auto'}),
        html.Div(id='model-accuracy-output-iris', className="lead text-center mt-4"),
        html.Div(id='prediction-output-iris', className="lead text-center mt-4"),
        html.Div(id='model-accuracy-output-penguins', className="lead text-center mt-4"),
        html.Div(id='prediction-output-penguins', className="lead text-center mt-4"),
    ])

fruitsView = html.Div(id="fruits",children=
                [
                    html.Div([
                        html.H1("Fruits Panel"),
                        "Insert a fruit",html.Br(),
                        html.Label(id="lbl-output"),
                        dcc.Dropdown(id="cb-insert",options=["apple","mango","banana","kiwi","pear","papaya"],multi=True,style={"width":"500px"}),
                        html.Button(id="btn-insert",children="Insert"),html.Br(),
                        html.Button(id="btn-flush",children="Flush fruits"),
                        html.Div(
                            id="div-dash-table",
                            children=[ 
                                "Current fruit list",html.Br(),
                                dash_table.DataTable(id='fruits-table',data=[],style_cell={'textAlign': 'center'})
                            ],style={'padding-top':'40px','width':'100%'}
                        )
                    ],style={'max-width': '700px','margin':'auto'})
                ]
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
    State('cb-model','value'),
    State('model-accuracy-output-iris','children'),
    State('prediction-output-iris','children'),
    State('cb-dataset','value'),
    prevent_initial_callback = True
)
def clearInputsIris(n_clicks,sepal_length,sepal_width,petal_length,petal_width,model,model_accuracy,prediction,dataset):
    if n_clicks:
        if dataset=="iris": 
            return [],[],"","","",""
    return model_accuracy,prediction,sepal_length,sepal_width,petal_length,petal_width,model

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
    State('cb-model','value'),
    State('model-accuracy-output-penguins','children'),
    State('prediction-output-penguins','children'),
    State('cb-dataset','value'),
    prevent_initial_callback = True
)
def clearInputsPenguins(n_clicks,island,culmen_length,culmen_depth,flipper_length,body_mass,sex,model,model_accuracy,prediction,dataset):
    if n_clicks:
        if dataset=="penguins": 
            return [],[],"","","","","","",""
    return model_accuracy,prediction,island,culmen_length,culmen_depth,flipper_length,body_mass,sex,model


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
    app.run_server(host='0.0.0.0', debug=True)