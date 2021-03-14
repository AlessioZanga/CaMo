import camo
import pandas as pd
import pytest


PC_DSEP = [
    (
        camo.data.sprites.education_fertility.sample(1000, seed=31),
        {
            ('ADOLF', 'DADSO'): set(),
            ('ADOLF', 'FARM'): set(),
            ('ADOLF', 'FEC'): set(),
            ('ADOLF', 'NOSIB'): set(),
            ('ADOLF', 'RACE'): set(),
            ('ADOLF', 'REGN'): set(),
            ('ADOLF', 'REL'): set(),
            ('ADOLF', 'YCIG'): set(),
            ('AGE', 'DADSO'): set(),
            ('AGE', 'FARM'): {'YCIG'},
            ('AGE', 'NOSIB'): {'RACE'},
            ('AGE', 'REL'): {'ADOLF', 'ED', 'FEC'},
            ('DADSO', 'ADOLF'): set(),
            ('DADSO', 'AGE'): set(),
            ('DADSO', 'ED'): set(),
            ('DADSO', 'FARM'): set(),
            ('DADSO', 'FEC'): set(),
            ('DADSO', 'RACE'): set(),
            ('DADSO', 'REGN'): set(),
            ('DADSO', 'REL'): {'REGN'},
            ('DADSO', 'YCIG'): set(),
            ('ED', 'DADSO'): set(),
            ('ED', 'FARM'): set(),
            ('ED', 'FEC'): set(),
            ('ED', 'NOSIB'): set(),
            ('ED', 'REL'): {'AGE', 'RACE', 'REGN'},
            ('FARM', 'ADOLF'): set(),
            ('FARM', 'AGE'): {'YCIG'},
            ('FARM', 'DADSO'): set(),
            ('FARM', 'ED'): set(),
            ('FARM', 'FEC'): set(),
            ('FARM', 'NOSIB'): set(),
            ('FARM', 'RACE'): set(),
            ('FARM', 'YCIG'): {'AGE'},
            ('FEC', 'ADOLF'): set(),
            ('FEC', 'DADSO'): set(),
            ('FEC', 'ED'): set(),
            ('FEC', 'FARM'): set(),
            ('FEC', 'NOSIB'): set(),
            ('FEC', 'RACE'): set(),
            ('FEC', 'REGN'): set(),
            ('FEC', 'REL'): set(),
            ('FEC', 'YCIG'): set(),
            ('NOSIB', 'ADOLF'): set(),
            ('NOSIB', 'AGE'): {'RACE'},
            ('NOSIB', 'ED'): set(),
            ('NOSIB', 'FARM'): set(),
            ('NOSIB', 'FEC'): set(),
            ('NOSIB', 'REGN'): set(),
            ('NOSIB', 'REL'): set(),
            ('NOSIB', 'YCIG'): set(),
            ('RACE', 'ADOLF'): set(),
            ('RACE', 'DADSO'): set(),
            ('RACE', 'FARM'): set(),
            ('RACE', 'FEC'): set(),
            ('RACE', 'REL'): set(),
            ('RACE', 'YCIG'): set(),
            ('REGN', 'ADOLF'): set(),
            ('REGN', 'DADSO'): set(),
            ('REGN', 'FEC'): set(),
            ('REGN', 'NOSIB'): set(),
            ('REGN', 'YCIG'): set(),
            ('REL', 'ADOLF'): set(),
            ('REL', 'AGE'): {'ADOLF', 'ED', 'FEC'},
            ('REL', 'DADSO'): {'REGN'},
            ('REL', 'ED'): {'AGE', 'RACE', 'REGN'},
            ('REL', 'FEC'): set(),
            ('REL', 'NOSIB'): set(),
            ('REL', 'RACE'): set(),
            ('REL', 'YCIG'): set(),
            ('YCIG', 'ADOLF'): set(),
            ('YCIG', 'DADSO'): set(),
            ('YCIG', 'FARM'): {'AGE'},
            ('YCIG', 'FEC'): set(),
            ('YCIG', 'NOSIB'): set(),
            ('YCIG', 'RACE'): set(),
            ('YCIG', 'REGN'): set(),
            ('YCIG', 'REL'): set()
        }
    ),
]

M = camo.LinearGaussianSCM(
    V=["A", "B", "C", "D"],
    Beta=[[0, 2, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]]
)

N = camo.LinearGaussianSCM.from_structure(
    V=["A", "B", "C", "D", "E"],
    E=[("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E")]
)

PC_FIT = []
for method in ["fisher_z", "student_t", "fast_fisher_z", "fast_student_t"]:
    PC_FIT.append((
        M.sample(1000, seed=31),
        method,
        {
            ("A", "B"), ("B", "A"),
            ("D", "B"), ("B", "D")
        }
    ))
    PC_FIT.append((
        N.sample(1000, seed=31),
        method,
        {
            ("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E"),
            ("B", "A"), ("C", "B"), ("D", "B"), ("E", "C"), ("E", "D")
        }
    ))

PC_FIT_TRANSFORM = []
for method in ["fisher_z", "student_t", "fast_fisher_z", "fast_student_t"]:
    PC_FIT_TRANSFORM.append((
        M.sample(1000, seed=31),
        method,
        None,
        {("A", "B")},
        {("A", "B"), ("B", "D")}
    ))


class TestPC:

    @pytest.mark.parametrize("data, T", PC_DSEP)
    def test_dsep(self, data, T):
        PC = camo.PC()
        PC.fit(data)
        assert dict(PC._dsep) == T

    @pytest.mark.parametrize("data, method, T", PC_FIT)
    def test_fit(self, data, method, T):
        G = camo.PC(method=method).fit(data)
        assert G.E == T

    @pytest.mark.parametrize("data, method, blacklist, whitelist, T", PC_FIT_TRANSFORM)
    def test_fit_transform(self, data, method, blacklist, whitelist, T):
        G = camo.PC(method=method).fit_transform(data, blacklist, whitelist)
        for t in T:
            assert G.is_tail_head(*t)
