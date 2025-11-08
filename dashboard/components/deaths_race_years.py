from dash import html, dcc 
import duckdb
from id import SCATTER_PLOT
import plotly.express as px 

def ScatterPlot() -> html.Div:
    with duckdb.connect("../data/deaths_in_nyc.ddb") as conn:
        df = conn.sql("""
            SELECT * FROM deaths;
        """).df()

    fig = px.scatter(df, x="Year", y="Deaths", facet_row="Sex", facet_col="Race Ethnicity", color="Leading Cause", opacity=0.5, title="<b>Deaths by Each Race and Sex Over Years</b>")
    fig.update_xaxes(matches=None)
    fig.update_yaxes(matches=None)
    fig.update_layout(
        height=800, title_x=0.5, font=dict(family="Arial", size=14, color="#888888"),
        legend=dict(title="Cause of Death", font=dict(family="Arial", size=10)),
    )
    return html.Div(id= SCATTER_PLOT, children=[
        dcc.Graph(figure=fig)
    ])



