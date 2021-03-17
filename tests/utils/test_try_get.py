from camo.utils import _try_get


class TestTryGet:

    def test_try_get_string(self):
        assert _try_get("A", {"A": 1}) == 1

    def test_try_get_other(self):
        f = lambda x: x
        assert _try_get(f, {"A": 1}) == f

    def test_try_get_exception(self):
        try:
            _try_get("B", {"A": 1})
            assert False
        except ValueError:
            assert True
