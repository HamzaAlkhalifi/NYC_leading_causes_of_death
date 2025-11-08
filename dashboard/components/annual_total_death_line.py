from dash import Input, Output, callback, dcc, html  
import duckdb
from id import ANNUAL_LINEPLOT, RACE_DD, GENDER_DD
import plotly.express as px
from plotly.subplots import make_subplots

def LinePlot() -> html.Div:
    @callback(
        Output(ANNUAL_LINEPLOT, "children"),
        [
            Input(RACE_DD, "value"),
            Input(GENDER_DD, "value")
        ]
    )
    def linePlot(races, genders) -> dcc.Graph | None: 
        if races != [] and genders != []:
            with duckdb.connect("../data/deaths_in_nyc.ddb") as conn:
                df = conn.sql(f"""
                    SELECT Year, "Leading Cause", SUM(Deaths) AS Total_Deaths
                    FROM deaths 
                    WHERE "Race Ethnicity" IN ({', '.join([f"'{race}'" for race in races])})
                        AND Sex IN ({', '.join([f"'{gender}'" for gender in genders])})
                    GROUP BY Year, "Leading Cause";
                """).df()

            df["Avg_Deaths"] = df["Total_Deaths"]
            year_death = df.groupby("Year").agg({"Total_Deaths":"sum", "Avg_Deaths": "mean"})
            
            fig = make_subplots(specs=[[{"secondary_y":True}]])
            total = px.line(year_death, x=year_death.index, y="Total_Deaths", line_shape="spline", color_discrete_sequence=['purple'])
            total.update_traces(line=dict(width=3))
            for trace in total.data:
                trace.name = "Total Deaths"
                trace.showlegend = True
                fig.add_trace(trace, secondary_y=False)

            avg = px.line(year_death, x=year_death.index, y="Avg_Deaths", color_discrete_sequence=['red'])
            avg.update_traces(line=dict(dash="dash", width=2), mode="lines+markers")
            for trace in avg.data:
                trace.name = "Average Deaths"
                trace.showlegend = True
                fig.add_trace(trace, secondary_y=True)

            fig.update_layout(title="<b>Annual Total Deaths & Average Deaths</b><br><sup>The AVG. of all the causes of death in a year</sup>", xaxis_title= "<b>Year</b>",
                              hovermode="x unified", font=dict(family="Arial", size=14, color="#888888"), height=600, showlegend=True, plot_bgcolor="white",
                                legend=dict(
                                    title="Metrics",
                                    orientation="h",
                                    yanchor="top",
                                    y=1.02,
                                    xanchor="right",
                                    x=1,
                                    bgcolor="white",
                                    font=dict(size=12, color="#888888")
                                )

                              )
            fig.update_yaxes(title="<b>Total Deaths</b>",secondary_y=False, showgrid=False)
            fig.update_yaxes(title="<b>AVG. Deaths</b>", secondary_y=True, showgrid= False)
            
            return dcc.Graph(figure=fig)
        else:
            return None
    return html.Div(id= ANNUAL_LINEPLOT)
