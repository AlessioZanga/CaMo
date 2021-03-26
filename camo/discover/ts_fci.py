import pandas as pd

from .augmented_fci import aFCI
from ..backend import tsPAG


class tsFCI(aFCI):

    _t_max: int

    def __init__(
        self,
        method: str = "fast_student_t",
        alpha: float = 0.05,
        t_max: int = 1
    ):
        super().__init__(method, alpha)
        self._t_max = t_max + 1

    def _shift_data(self, data: pd.DataFrame) -> pd.DataFrame:
        shifted = data.copy()
        columns = data.columns
        shifted.columns = [c + ":0" for c in columns]

        for i in range(1, self._t_max):
            shift = data.shift(-i)
            shift.columns = [c + f":{i}" for c in columns]
            shifted = pd.concat([shifted, shift], axis=1)

        shifted = shifted[:-self._t_max+1]
        shifted.index.name = "tsPAG"

        return shifted

    def fit(self, data: pd.DataFrame) -> tsPAG:
        return super().fit(self._shift_data(data))
