import plotly.express as px
from dash import dcc, Input, Output, callback, html
import dash_bootstrap_components as dbc
import duckdb 
from id import ANNUAL_BARCHART, RACE_DD, GENDER_DD



def BarChart() -> html.Div:
    @callback(
        Output(ANNUAL_BARCHART, "children"),
        [Input(GENDER_DD, "value"),
        Input(RACE_DD, "value")]
    )
    def barChart(genders, races) -> dcc.Graph | dbc.Alert:
        if genders != [] and races != []:
            with duckdb.connect("../data/deaths_in_nyc.ddb") as conn:
                df= conn.sql(f"""
                    SELECT * FROM deaths 
                    WHERE Sex IN ({", ".join(f"'{gender}'" for gender in genders)}) AND "Race Ethnicity" IN ({", ".join(f"'{race}'" for race in races)})
                """).df()

            cause_death = df.groupby(["Year","Leading Cause"]).agg({"Deaths":"sum"}).reset_index()
            cause_death = cause_death.groupby("Leading Cause").agg({"Deaths":"mean"})
            cause_death = cause_death.sort_values("Deaths", ascending=False).head()

            fig = px.bar(
                cause_death, x=cause_death.index, y="Deaths", hover_name=cause_death.index, hover_data=["Deaths"],
                color_discrete_sequence=["#4C8A4C"]
            )
            fig.update_layout(
                xaxis_title="<b>Cause of Death</b>", yaxis_title="<b>Average Deaths</b>", plot_bgcolor="white", 
                height=600, title="<b>Highest 5 Causes by Average Annual Death</b>", bargap=0.1, xaxis_showgrid=False, yaxis_showgrid=False,
                font=dict(family="Arial", color="#888888", size=14)
            )
            fig.update_traces(marker=dict(line=dict(width=0)))
            return dcc.Graph(figure=fig)
        else:
            return dbc.Alert("Select From The Dropdown...", color="warning")
    return html.Div(id= ANNUAL_BARCHART)
