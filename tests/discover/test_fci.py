import io
import camo
import pandas as pd

T = io.StringIO("""
,ADOLF,AGE,DADSO,ED,FEC,NOSIB,RACE,REGN,REL,YCIG
ADOLF,0,2,0,2,0,0,0,0,0,0
AGE,1,0,0,2,1,0,1,2,0,1
DADSO,0,0,0,2,0,1,0,0,0,0
ED,1,2,1,0,0,1,2,0,0,1
FEC,0,2,0,0,0,0,0,0,0,0
NOSIB,0,0,1,2,0,0,0,0,0,0
RACE,0,2,0,2,0,0,0,2,0,0
REGN,0,2,0,0,0,0,2,0,1,0
REL,0,0,0,0,0,0,0,2,0,0
YCIG,0,2,0,2,0,0,0,0,0,0
""")
T = pd.read_csv(T, index_col=0)
T = (T, {
    ("ADOLF", "AGE"): {"ED"},
    ("ADOLF", "ED"): {"AGE"},
    ("AGE", "ADOLF"): {"ED", "FEC", "RACE", "REGN", "YCIG"},
    ("AGE", "ED"): {"ADOLF", "FEC", "RACE", "REGN", "YCIG"},
    ("AGE", "FEC"): {"ADOLF", "ED", "RACE", "REGN", "YCIG"},
    ("AGE", "RACE"): {"ADOLF", "ED", "FEC", "REGN", "YCIG"},
    ("AGE", "REGN"): {"ADOLF", "ED", "FEC", "RACE", "YCIG"},
    ("AGE", "YCIG"): {"ADOLF", "ED", "FEC", "RACE", "REGN"},
    ("DADSO", "ED"): {"NOSIB"},
    ("DADSO", "NOSIB"): {"ED"},
    ("ED", "ADOLF"): {"AGE", "DADSO", "NOSIB", "RACE", "YCIG"},
    ("ED", "AGE"): {"ADOLF", "DADSO", "NOSIB", "RACE", "YCIG"},
    ("ED", "DADSO"): {"ADOLF", "AGE", "NOSIB", "RACE", "YCIG"},
    ("ED", "NOSIB"): {"ADOLF", "AGE", "DADSO", "RACE", "YCIG"},
    ("ED", "RACE"): {"ADOLF", "AGE", "DADSO", "NOSIB", "YCIG"},
    ("ED", "YCIG"): {"ADOLF", "AGE", "DADSO", "NOSIB", "RACE"},
    ("FEC", "AGE"): set(),
    ("NOSIB", "DADSO"): {"ED"},
    ("NOSIB", "ED"): {"DADSO"},
    ("RACE", "AGE"): {"ED", "REGN"},
    ("RACE", "ED"): {"AGE", "REGN"},
    ("RACE", "REGN"): {"AGE", "ED"},
    ("REGN", "AGE"): {"RACE", "REL"},
    ("REGN", "RACE"): {"AGE", "REL"},
    ("REGN", "REL"): {"AGE", "RACE"},
    ("REL", "REGN"): set(),
    ("YCIG", "AGE"): {"ED"},
    ("YCIG", "ED"): {"AGE"}
})
