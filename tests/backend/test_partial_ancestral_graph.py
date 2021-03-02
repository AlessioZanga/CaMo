import camo
import pytest


EP = camo.Endpoints

DDPs = [
    (
        [
            ("E", "F"), ("F", "G"), ("G", "A"), ("A", "B"),
            ("A", "C"), ("B", "C"), ("F", "B"), ("G", "B")
        ], # Edges
        [
            ("E", "F", EP.HEAD), ("F", "G", EP.HEAD), ("G", "A", EP.HEAD),
            ("A", "B", EP.HEAD), ("A", "C", EP.HEAD), ("B", "C", EP.CIRCLE),
            ("F", "E", EP.CIRCLE), ("G", "F", EP.HEAD), ("A", "G", EP.HEAD),
            ("B", "A", EP.TAIL), ("C", "A", EP.HEAD), ("C", "B", EP.CIRCLE),
            ("F", "B", EP.HEAD), ("G", "B", EP.HEAD), ("B", "F", EP.TAIL),
            ("B", "G", EP.TAIL)
        ], # Endpoints
        ("E", "C", "B"), # Definite discriminating paths
        [("E", "F", "G", "A", "C", "B")] # T
    ),
    (
        [
            ("X_l", "X_k"), ("X_k", "X_j"), ("X_j", "X_b"),
            ("X_k", "X_p"), ("X_j", "X_p"), ("X_b", "X_p")
        ],
        [
            ("X_l", "X_k", EP.HEAD), ("X_k", "X_l", EP.HEAD),
            ("X_k", "X_j", EP.HEAD), ("X_j", "X_k", EP.HEAD),
            ("X_j", "X_b", EP.CIRCLE), ("X_b", "X_j", EP.HEAD),
            ("X_k", "X_p", EP.HEAD), ("X_p", "X_k", EP.TAIL),
            ("X_j", "X_p", EP.HEAD), ("X_p", "X_j", EP.TAIL),
            ("X_b", "X_p", EP.HEAD), ("X_p", "X_b", EP.CIRCLE)
        ],
        ("X_l", "X_b", "X_p"),
        [("X_l", "X_k", "X_j", "X_b", "X_p")]
    )
]


class TestPartialAncestralGraph:

    @pytest.mark.parametrize("E, EP, DDP, T", DDPs)
    def test_definite_discriminating_path(self, E, EP, DDP, T):
        M = camo.PAG(E=E)
        for ep in EP:
            M.set_endpoint(*ep)
        ddp = [
            p for p in M.paths(DDP[0], DDP[2])
            if M.is_discriminating_path(p, DDP[1])
        ]
        assert ddp == T
