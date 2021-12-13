import argparse
from pathlib import Path

import yaml
import selenium

# local (add flag_recognition to your PYTHONPATH)
from common.utils import readfile


def parse_args():
    parser = argparse.ArgumentParser()

    cur_file = Path(__file__).absolute()
    default_conf = cur_file.parent / "conf" / (cur_file.stem + ".yml")
    parser.add_argument(
        "--conf", default=default_conf,
    )
    return parser.parse_args()

class DownloadFlags:
    def __init__(self, conf):
        print (conf)

    def main(self):
        pass

if __name__ == "__main__":
    args = parse_args()
    conf = readfile(args.conf)
    DF = DownloadFlags(conf)
