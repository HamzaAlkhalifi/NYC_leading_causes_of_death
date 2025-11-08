from dash import dcc
import duckdb
from id import RACE_DD

def RaceDropDown() -> dcc.Dropdown:
    with duckdb.connect("../data/deaths_in_nyc.ddb") as conn:
        races= conn.sql('SELECT DISTINCT "Race Ethnicity" FROM deaths').fetchall()
        races = [r[0] for r in races]
        
    return dcc.Dropdown(
        options= [{"label":race, "value":race} for race in races],
        multi= True,
        value= races,
        id= RACE_DD
    )
