from dash import dcc 
import duckdb
from id import GENDER_DD

def GenderDropDown() -> dcc.Dropdown:
    with duckdb.connect("../data/deaths_in_nyc.ddb") as conn:
        genders= conn.sql("SELECT DISTINCT Sex FROM deaths").fetchall()
        genders= [gender[0] for gender in genders]

    return dcc.Dropdown(
        options= [{"label":gender, "value":gender} for gender in genders],
        multi= True,
        value= genders,
        id= GENDER_DD
    )
