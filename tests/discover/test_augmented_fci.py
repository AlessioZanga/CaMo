import io
import camo
import pandas as pd
import pytest


EP = camo.Endpoints

aFCI_RULES = [
    (
        5,
        [   # A o-o B o-o C o-o D o-o A
            ("A", "B", EP.CIRCLE), ("B", "A", EP.CIRCLE),
            ("B", "C", EP.CIRCLE), ("C", "B", EP.CIRCLE),
            ("C", "D", EP.CIRCLE), ("D", "C", EP.CIRCLE),
            ("D", "A", EP.CIRCLE), ("A", "D", EP.CIRCLE),
        ],
        [   # A --- B --- C --- D --- A
            ("A", "B", EP.TAIL), ("B", "A", EP.TAIL),
            ("B", "C", EP.TAIL), ("C", "B", EP.TAIL),
            ("C", "D", EP.TAIL), ("D", "C", EP.TAIL),
            ("D", "A", EP.TAIL), ("A", "D", EP.TAIL),
        ]
    ),
    (
        6,
        [   # A --- B o--* C
            ("A", "B", EP.TAIL), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.CIRCLE),
        ],
        [   # A --- B ---* C
            ("A", "B", EP.TAIL), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
        ]
    ),
    (
        7,
        [   # A --o B o-* C and A -x- C
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.CIRCLE),
        ],
        [   # A --o B --* C
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
        ]
    ),
    (
        8,
        [   # A --> B --> C and A o-> C
            ("A", "B", EP.HEAD), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.CIRCLE),
        ],
        [   # A --> C
            ("A", "B", EP.HEAD), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.TAIL),
        ]
    ),
    (
        8,
        [   # A --o B --> C and A o-> C
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.CIRCLE),
        ],
        [   # A --> C
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.TAIL),
        ]
    ),
    (
        9,
        [   # A o-> D and A *-> B ... C *-> D
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.CIRCLE), ("C", "B", EP.TAIL),
            ("C", "D", EP.CIRCLE), ("D", "C", EP.TAIL),
            ("D", "A", EP.CIRCLE), ("A", "D", EP.HEAD),
        ],
        [   # A --> D
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.CIRCLE), ("C", "B", EP.TAIL),
            ("C", "D", EP.CIRCLE), ("D", "C", EP.TAIL),
            ("D", "A", EP.TAIL), ("A", "D", EP.HEAD),
        ]
    ),
    (
        10,
        [   # A o-> F and A *-> B ... C --> F and A *-> D ... E --> F
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "D", EP.CIRCLE), ("D", "A", EP.TAIL),
            ("D", "E", EP.HEAD), ("E", "D", EP.TAIL),
            ("A", "F", EP.HEAD), ("F", "A", EP.CIRCLE),
            ("C", "F", EP.HEAD), ("F", "C", EP.TAIL),
            ("E", "F", EP.HEAD), ("F", "E", EP.TAIL),
        ],
        [   # A --> F
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "D", EP.CIRCLE), ("D", "A", EP.TAIL),
            ("D", "E", EP.HEAD), ("E", "D", EP.TAIL),
            ("A", "F", EP.HEAD), ("F", "A", EP.TAIL),
            ("C", "F", EP.HEAD), ("F", "C", EP.TAIL),
            ("E", "F", EP.HEAD), ("F", "E", EP.TAIL),
        ]
    )
]

EDUCATION_FERTILITY = camo.data.sprites.education_fertility.sample(1000, seed=31)
PUBLISHING_PRODUCTIVITY = camo.data.sprites.publishing_productivity.sample(1000, seed=31)

aFCI_FIT_TRANSFORM = [
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


class TestAugmentedFCI:

    @pytest.mark.parametrize("R, E, T", aFCI_RULES)
    def test_rules(self, R, E, T):
        G = camo.PAG(E=[e[:2] for e in E])
        for e in E:
            G.set_endpoint(*e)
        aFCI = camo.AugmentedFCI()
        getattr(aFCI, f"_R{R}")(G)
        for t in T:
            assert G.has_endpoint(*t)

    @pytest.mark.parametrize("data, T", aFCI_FIT_TRANSFORM)
    def test_fit_transform(self, data, T):
        G = camo.AugmentedFCI().fit_transform(data)
        G = G.to_adjacency_matrix()
        pd.testing.assert_frame_equal(G, T)
