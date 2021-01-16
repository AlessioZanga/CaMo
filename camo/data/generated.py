from os import listdir
from os.path import dirname, join, sep
import sys

import pandas as pd


for file in listdir(dirname(__file__)):
    if file.endswith(".gz"):
        setattr(
            sys.modules[__name__],
            file.split(sep)[-1][:-3],
            pd.read_csv(join(dirname(__file__), file))
        )
