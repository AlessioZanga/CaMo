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
            ("B", "A", EP.HEAD), ("C", "A", EP.TAIL), ("C", "B", EP.CIRCLE),
            ("F", "B", EP.HEAD), ("G", "B", EP.HEAD), ("B", "F", EP.TAIL),
            ("B", "G", EP.TAIL)
        ], # Endpoints
        ("E", "C", "B"), # Definite discriminating paths
        [("E", "F", "G", "A", "C", "B")] # T
    )
]


class TestPartialAncestralGraph:

    @pytest.mark.parametrize("E, EP, DDP, T", DDPs)
    def test_definite_discriminating_path(self, E, EP, DDP, T):
        M = camo.PartialAncestralGraph(E=E)
        for ep in EP:
            M.set_endpoint(*ep)
        assert M.all_definite_discriminating_paths(*DDP) == T
