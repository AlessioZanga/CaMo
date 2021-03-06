import io
import camo
import pandas as pd
import pytest


EP = camo.Endpoints

CI_RULES = [
    (
        1,
        [   # A *-> B o-* C and A -x- C
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.HEAD), ("C", "B", EP.CIRCLE),
        ],
        [   # A *-> B --> C
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
        ]
    ),
    (
        2,
        [   # A --> B *-> C and A *-o C
            ("A", "B", EP.HEAD), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.CIRCLE),
            ("A", "C", EP.CIRCLE), ("C", "A", EP.CIRCLE),
        ],
        [   # A *-> C
            ("A", "B", EP.HEAD), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.CIRCLE),
            ("A", "C", EP.HEAD), ("C", "A", EP.CIRCLE),
        ]
    ),
    (
        2,
        [   # A *-> B --> C and A *-o C
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.CIRCLE), ("C", "A", EP.CIRCLE),
        ],
        [   # A *-> C
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.CIRCLE),
        ]
    ),
    (
        3,
        [   # A *-> B <-* C and A *-o D o-* C and A -x- C and D *-o B
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.CIRCLE), ("C", "B", EP.HEAD),
            ("A", "D", EP.CIRCLE), ("D", "A", EP.CIRCLE),
            ("B", "D", EP.CIRCLE), ("D", "B", EP.CIRCLE),
            ("C", "D", EP.CIRCLE), ("D", "C", EP.CIRCLE),
        ],
        [   # D *-> B
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.CIRCLE), ("C", "B", EP.HEAD),
            ("A", "D", EP.CIRCLE), ("D", "A", EP.CIRCLE),
            ("B", "D", EP.CIRCLE), ("D", "B", EP.HEAD),
            ("C", "D", EP.CIRCLE), ("D", "C", EP.CIRCLE),
        ]
    ),
]

CI_RULES_DSEP = [
    (
        0,
        [   # A o-o B o-o C and A -x- C and B not in dsep(A, C)
            ("A", "B", EP.CIRCLE), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.CIRCLE), ("C", "B", EP.CIRCLE),
        ],
        [
            ("A", "C", set())
        ],
        [   # A *-> B <-* C
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.CIRCLE), ("C", "B", EP.HEAD),
        ]
    ),
    (
        4,
        [   # A *-> B <-> C o-o D and B --> D and C in dsep(A, D)
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.HEAD), ("C", "B", EP.HEAD),
            ("C", "D", EP.CIRCLE), ("D", "C", EP.CIRCLE),
            ("B", "D", EP.TAIL), ("D", "B", EP.HEAD),
        ],
        [
            ("A", "B", set(["C"]))
        ],
        [   # C --> D
            ("A", "B", EP.HEAD), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.HEAD), ("C", "B", EP.HEAD),
            ("C", "D", EP.CIRCLE), ("D", "C", EP.CIRCLE),
            ("B", "D", EP.TAIL), ("D", "B", EP.HEAD),
        ]
    )
]

CI_FIT_TRANSFORM = [
    (
        camo.data.sprites.education_fertility.sample(1000, seed=31),
        pd.read_csv(
            io.StringIO(
"""
,ADOLF,AGE,DADSO,ED,FARM,FEC,NOSIB,RACE,REGN,REL,YCIG
ADOLF,0,2,0,2,0,0,0,0,0,0,0
AGE,1,0,0,2,0,1,0,3,2,0,1
DADSO,0,0,0,0,0,0,2,0,0,0,0
ED,1,2,0,0,0,0,0,2,2,0,1
FARM,0,0,0,0,0,0,0,0,2,1,0
FEC,0,2,0,0,0,0,0,0,0,0,0
NOSIB,0,0,1,0,0,0,0,2,0,0,0
RACE,0,2,0,2,0,0,2,0,2,0,0
REGN,0,2,0,2,1,0,0,2,0,1,0
REL,0,0,0,0,1,0,0,0,2,0,0
YCIG,0,2,0,2,0,0,0,0,0,0,0
"""
            ),
            index_col=0
        )
    )
]


class TestCI:

    @pytest.mark.parametrize("R, E, T", CI_RULES)
    def test_rules(self, R, E, T):
        G = camo.PAG(E=[e[:2] for e in E])
        for e in E:
            G.set_endpoint(*e)
        CI = camo.CI()
        getattr(CI, f"_R{R}")(G)
        for t in T:
            assert G.has_endpoint(*t)

    @pytest.mark.parametrize("R, E, S, T", CI_RULES_DSEP)
    def test_rules_dsep(self, R, E, S, T):
        G = camo.PAG(E=[e[:2] for e in E])
        for e in E:
            G.set_endpoint(*e)
        CI = camo.CI()
        for (u, v, s) in S:
            CI._dsep[(u, v)] = s
        getattr(CI, f"_R{R}")(G)
        for t in T:
            assert G.has_endpoint(*t)

    @pytest.mark.parametrize("data, T", CI_FIT_TRANSFORM)
    def test_fit_transform(self, data, T):
        G = camo.CI().fit_transform(data)
        G = G.to_adjacency_matrix()
        pd.testing.assert_frame_equal(G, T)
