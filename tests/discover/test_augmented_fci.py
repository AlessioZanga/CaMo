import camo
import pytest


EP = camo.Endpoints

RULES = [
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
            ("A", "C", EP.HEAD), ("C", "A", EP.CIRCLE)
        ],
        [   # A --> C
            ("A", "B", EP.HEAD), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.TAIL)
        ]
    ),
    (
        8,
        [   # A --o B --> C and A o-> C
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.CIRCLE)
        ],
        [   # A --> C
            ("A", "B", EP.CIRCLE), ("B", "A", EP.TAIL),
            ("B", "C", EP.HEAD), ("C", "B", EP.TAIL),
            ("A", "C", EP.HEAD), ("C", "A", EP.TAIL)
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


class TestAugmentedFCI:

    @pytest.mark.parametrize("R, E, T", RULES)
    def test_rules(self, R, E, T):
        G = camo.PAG(E=[e[:2] for e in E])
        for e in E:
            G.set_endpoint(*e)
        aFCI = camo.AugmentedFCI()
        getattr(aFCI, f"_R{R}")(G)
        for t in T:
            assert G.has_endpoint(*t)
