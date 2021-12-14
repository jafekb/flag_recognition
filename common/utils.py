import json
import os
from pathlib import Path
from typing import Union

import numpy as np
from typeguard import typechecked
import yaml


@typechecked
def readfile(fname: Union[str, Path]) -> Union[str, dict, np.ndarray]:
    """
    Util function for reading a variety of different files
    """
    fname = str(fname)
    ext = os.path.splitext(fname)[-1]
    if ext == ".json":
        with open(fname, "r") as f_in:
            data = json.load(f_in)
    elif ext == ".txt":
        with open(fname, "r") as f_in:
            data = f_in.read()
    elif ext == ".bin":
        # point clouds
        data = np.fromfile(fname, dtype=np.float32).reshape(-1, 4)
    elif ext in (".yaml", ".yml"):
        with open(fname, "r") as f_in:
            data = yaml.safe_load(f_in)
    else:
        raise ValueError(f"function readfile cannot handle file '{fname}'")

    return data
