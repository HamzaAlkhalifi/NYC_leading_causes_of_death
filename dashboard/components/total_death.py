from dash import callback, Output, Input, html, dcc
import duckdb
import plotly.express as px
from id import TOTAL_TREEMAP, RACE_DD, GENDER_DD

def TreeMap() -> html.Div:
    @callback(
        Output(TOTAL_TREEMAP, "children"),
        [
            Input(RACE_DD, "value"),
            Input(GENDER_DD, "value")
        ]
    )
    def treeMap(races, genders) -> dcc.Graph | None:
        if races != [] and genders != []:
            with duckdb.connect("../data/deaths_in_nyc.ddb") as conn:
                df = conn.sql(f"""
                    SELECT * FROM deaths 
                    WHERE "Race Ethnicity" IN ({', '.join([f"'{race}'" for race in races])})
                        AND Sex IN ({', '.join([f"'{gender}'" for gender in genders])})
                """).df()

            fig = px.treemap(df, path=["Race Ethnicity", "Sex", "Leading Cause"], values="Deaths", title= "<b>Total Deaths by Causes</b>")
            fig.update_layout(height=600, font=dict(family="Arial", color="#888888", size=14))  
            return dcc.Graph(figure=fig)
        else:
            return None

    return html.Div(id= TOTAL_TREEMAP)
