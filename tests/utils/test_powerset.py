from camo.utils import _powerset


class TestPowerset:

    def test_powerset(self):
        assert list(_powerset(range(3))) == [
            set(),
            {0}, {1}, {2},
            {0, 1}, {0, 2}, {1, 2},
            {0, 1, 2},
        ]
