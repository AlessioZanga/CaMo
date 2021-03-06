import io
import camo
import pandas as pd
import pytest


EDUCATION_FERTILITY = camo.data.sprites.education_fertility.sample(1000, seed=31)
PUBLISHING_PRODUCTIVITY = camo.data.sprites.publishing_productivity.sample(1000, seed=31)

FCI_PDSEP = [
    (
        EDUCATION_FERTILITY,
        {
            "ADOLF": {"AGE", "ED", "FARM", "FEC", "NOSIB", "RACE", "REGN", "REL", "YCIG"},
            "AGE": {"ADOLF", "ED", "FARM", "FEC", "NOSIB", "RACE", "REGN", "REL", "YCIG"},
            "DADSO": {"NOSIB"},
            "ED": {"ADOLF", "AGE", "FARM", "FEC", "NOSIB", "RACE", "REGN", "REL", "YCIG"},
            "FARM": {"ADOLF", "AGE", "ED", "FEC", "NOSIB", "RACE", "REGN", "REL", "YCIG"},
            "FEC": {"ADOLF", "AGE", "ED", "FARM", "NOSIB", "RACE", "REGN", "REL", "YCIG"},
            "NOSIB": {"ADOLF", "AGE", "DADSO", "ED", "FARM", "FEC", "RACE", "REGN", "REL", "YCIG"},
            "RACE": {"ADOLF", "AGE", "ED", "FARM", "FEC", "NOSIB", "REGN", "REL", "YCIG"},
            "REGN": {"ADOLF", "AGE", "ED", "FARM", "FEC", "NOSIB", "RACE", "REL", "YCIG"},
            "REL": {"ADOLF", "AGE", "ED", "FARM", "FEC", "NOSIB", "RACE", "REGN", "YCIG"},
            "YCIG": {"ADOLF", "AGE", "ED", "FARM", "FEC", "NOSIB", "RACE", "REGN", "REL"}
        }
    )
]

FCI_FIT = [
    (
        EDUCATION_FERTILITY,
        pd.read_csv(
            io.StringIO(
"""
,ADOLF,AGE,DADSO,ED,FARM,FEC,NOSIB,RACE,REGN,REL,YCIG
ADOLF,0,2,0,0,0,0,0,0,0,0,0
AGE,1,0,0,1,0,1,0,1,2,0,1
DADSO,0,0,0,0,0,0,2,0,0,0,0
ED,0,2,0,0,0,0,0,2,2,0,1
FARM,0,0,0,0,0,0,0,0,2,0,0
FEC,0,2,0,0,0,0,0,0,0,0,0
NOSIB,0,0,1,0,0,0,0,2,0,0,0
RACE,0,2,0,2,0,0,2,0,2,0,0
REGN,0,2,0,2,1,0,0,2,0,1,0
REL,0,0,0,0,0,0,0,0,2,0,0
YCIG,0,2,0,2,0,0,0,0,0,0,0
"""
            ),
            index_col=0
        )
    ),
    (
        PUBLISHING_PRODUCTIVITY,
        pd.read_csv(
            io.StringIO(
"""
,ABILITY,CITES,GPQ,PREPROD,PUBS,QFJ,SEX
ABILITY,0,2,1,0,0,2,2
CITES,2,0,0,1,2,2,0
GPQ,2,0,0,0,0,0,0
PREPROD,0,2,0,0,0,0,0
PUBS,0,2,0,0,0,2,2
QFJ,2,2,0,0,1,0,1
SEX,2,0,0,0,2,2,0
"""
            ),
            index_col=0
        )

    ),
]

FCI_FIT_TRANSFORM = [
    (
        EDUCATION_FERTILITY,
        pd.read_csv(
            io.StringIO(
"""
,ADOLF,AGE,DADSO,ED,FARM,FEC,NOSIB,RACE,REGN,REL,YCIG
ADOLF,0,2,0,0,0,0,0,0,0,0,0
AGE,1,0,0,2,0,1,0,3,2,0,1
DADSO,0,0,0,0,0,0,2,0,0,0,0
ED,0,2,0,0,0,0,0,2,2,0,1
FARM,0,0,0,0,0,0,0,0,2,0,0
FEC,0,2,0,0,0,0,0,0,0,0,0
NOSIB,0,0,1,0,0,0,0,2,0,0,0
RACE,0,2,0,2,0,0,2,0,2,0,0
REGN,0,2,0,2,1,0,0,2,0,1,0
REL,0,0,0,0,0,0,0,0,2,0,0
YCIG,0,2,0,2,0,0,0,0,0,0,0
"""
            ),
            index_col=0
        )
    ),
    (
        PUBLISHING_PRODUCTIVITY,
        pd.read_csv(
            io.StringIO(
"""
,ABILITY,CITES,GPQ,PREPROD,PUBS,QFJ,SEX
ABILITY,0,2,1,0,0,2,2
CITES,2,0,0,1,2,2,0
GPQ,2,0,0,0,0,0,0
PREPROD,0,2,0,0,0,0,0
PUBS,0,2,0,0,0,2,2
QFJ,2,2,0,0,1,0,1
SEX,2,0,0,0,2,2,0
"""
            ),
            index_col=0
        )
    ),
]


class TestFCI:

    @pytest.mark.skip(reason="No way of currently testing this.")
    @pytest.mark.parametrize("data, T", FCI_PDSEP)
    def test_pdsep(self, data, T):
        FCI = camo.FCI()
        FCI.fit(data)
        assert dict(FCI._pdsep) == T

    @pytest.mark.parametrize("data, T", FCI_FIT)
    def test_fit(self, data, T):
        G = camo.FCI().fit(data)
        G = G.to_adjacency_matrix()
        pd.testing.assert_frame_equal(G, T)

    @pytest.mark.parametrize("data, T", FCI_FIT_TRANSFORM)
    def test_fit_transform(self, data, T):
        G = camo.FCI().fit_transform(data)
        G = G.to_adjacency_matrix()
        pd.testing.assert_frame_equal(G, T)
