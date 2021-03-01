import camo
import pandas as pd
import pytest

from io import StringIO

EDUCATION_FERTILITY = camo.data.sprites.education_fertility.sample(1000, seed=31)

FCI_FIT = [
    (EDUCATION_FERTILITY,
    {
        ('ADOLF', 'AGE'): set(),
        ('AGE', 'ADOLF'): {'ED', 'FEC', 'RACE', 'REGN', 'YCIG'},
        ('AGE', 'ED'): {'ADOLF', 'FEC', 'RACE', 'REGN', 'YCIG'},
        ('AGE', 'FEC'): {'ADOLF', 'ED', 'RACE', 'REGN', 'YCIG'},
        ('AGE', 'RACE'): {'ADOLF', 'ED', 'FEC', 'REGN', 'YCIG'},
        ('AGE', 'REGN'): {'ADOLF', 'ED', 'FEC', 'RACE', 'YCIG'},
        ('AGE', 'YCIG'): {'ADOLF', 'ED', 'FEC', 'RACE', 'REGN'},
        ('DADSO', 'NOSIB'): set(),
        ('ED', 'AGE'): {'RACE', 'REGN', 'YCIG'},
        ('ED', 'RACE'): {'AGE', 'REGN', 'YCIG'},
        ('ED', 'REGN'): {'AGE', 'RACE', 'YCIG'},
        ('ED', 'YCIG'): {'AGE', 'RACE', 'REGN'},
        ('FARM', 'REGN'): set(),
        ('FEC', 'AGE'): set(),
        ('NOSIB', 'DADSO'): {'RACE'},
        ('NOSIB', 'RACE'): {'DADSO'},
        ('RACE', 'AGE'): {'ED', 'NOSIB', 'REGN'},
        ('RACE', 'ED'): {'AGE', 'NOSIB', 'REGN'},
        ('RACE', 'NOSIB'): {'AGE', 'ED', 'REGN'},
        ('RACE', 'REGN'): {'AGE', 'ED', 'NOSIB'},
        ('REGN', 'AGE'): {'ED', 'FARM', 'RACE', 'REL'},
        ('REGN', 'ED'): {'AGE', 'FARM', 'RACE', 'REL'},
        ('REGN', 'FARM'): {'AGE', 'ED', 'RACE', 'REL'},
        ('REGN', 'RACE'): {'AGE', 'ED', 'FARM', 'REL'},
        ('REGN', 'REL'): {'AGE', 'ED', 'FARM', 'RACE'},
        ('REL', 'REGN'): set(),
        ('YCIG', 'AGE'): {'ED'},
        ('YCIG', 'ED'): {'AGE'}
    })
]

FCI_FIT_TRANSFORM = [
    (EDUCATION_FERTILITY, """
    ,ADOLF,AGE,DADSO,ED,FARM,FEC,NOSIB,RACE,REGN,REL,YCIG
    ADOLF,0,2,0,2,0,0,0,0,0,0,0
    AGE,1,0,0,2,0,1,0,1,2,0,1
    DADSO,0,0,0,2,0,0,1,0,0,0,0
    ED,1,2,1,0,0,0,1,2,0,0,1
    FARM,0,0,0,0,0,0,0,0,2,0,0
    FEC,0,2,0,0,0,0,0,0,0,0,0
    NOSIB,0,0,1,2,0,0,0,0,0,0,0
    RACE,0,2,0,2,0,0,0,0,2,0,0
    REGN,0,2,0,0,1,0,0,2,0,1,0
    REL,0,0,0,0,0,0,0,0,2,0,0
    YCIG,0,2,0,2,0,0,0,0,0,0,0
    """)
]
