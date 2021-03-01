import sys
from os import listdir
from os.path import dirname, join, sep

import pandas as pd

from . import primer
from . import sprites

for file in listdir(dirname(__file__)):
    if file.endswith(".gz"):
        setattr(
            sys.modules[__name__],
            file.split(sep)[-1][:-3],
            pd.read_csv(join(dirname(__file__), file))
        )
