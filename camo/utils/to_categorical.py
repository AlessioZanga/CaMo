from collections import defaultdict
from typing import Dict, Tuple

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def _to_categorical(data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    encorders = defaultdict(LabelEncoder)
    data = data.apply(lambda x: encorders[x.name].fit_transform(x))
    return data, encorders
    