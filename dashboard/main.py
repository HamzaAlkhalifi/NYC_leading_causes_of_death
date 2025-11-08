from dash import Dash 
import dash_bootstrap_components as dbc 
from filters import RaceDropDown, GenderDropDown
from components import BarChart, LinePlot, TreeMap, ScatterPlot

def layouts() -> dbc.Container:
    container = dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col([RaceDropDown()]),
            dbc.Col([GenderDropDown()]),
        ]),
        dbc.Row([
            dbc.Col([BarChart()]),
            dbc.Col([LinePlot()]),
            dbc.Col([TreeMap()]),
        ]),
        dbc.Col([ScatterPlot()]),
    ])
    return container

def main() -> None:
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = layouts()
    app.run(debug=True)

if __name__ == "__main__":
    main()
