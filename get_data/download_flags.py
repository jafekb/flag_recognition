"""

"""
import argparse
from pathlib import Path
import urllib.request

import yaml
import selenium
from selenium import webdriver

# local (add flag_recognition to your PYTHONPATH)
from common.utils import readfile

# debug
import time
from pprint import pprint
import pdb


def parse_args():
    parser = argparse.ArgumentParser()

    cur_file = Path(__file__).absolute()
    default_conf = cur_file.parent / "conf" / (cur_file.stem + ".yml")
    parser.add_argument(
        "--conf", default=default_conf,
    )
    return parser.parse_args()

class DownloadFlags:
    """

    """
    def __init__(self, conf):
        """

        """
        self._pages = conf["pages"]
        self._drive_path = conf["chromedriver"]

    def __del__(self):
        """

        """
        self._driver.close()

    def download_and_tag_all_images(self):
        """

        """
        self._driver = webdriver.Chrome(self._drive_path)
        for page in self._pages:
            # There are so many images, this page usually takes a sec to load
            self._driver.get(page)

            images = self._driver.find_elements_by_tag_name('img')
            for image in images:
                src = image.get_attribute("src")
                if "flag" not in src.lower():
                    # They're usually pretty well-named
                    #  (TODO(jafek.ben) right?)
                    print (src)
                    continue
                urllib.request.urlretrieve(src, "image")
                return



if __name__ == "__main__":
    args = parse_args()
    conf = readfile(args.conf)
    DF = DownloadFlags(conf)
    DF.download_and_tag_all_images()
