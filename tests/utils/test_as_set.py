from camo.utils import _as_set


class TestAsSet:

    def test_none(self):
        assert _as_set(None) == set()

    def test_string(self):
        assert _as_set("string") == {"string"}

    def test_iterable(self):
        assert _as_set((0, 1, 2)) == {0, 1, 2}
        assert _as_set([0, 1, 2]) == {0, 1, 2}
        assert _as_set(range(3))  == {0, 1, 2}
