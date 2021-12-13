"""
Downloads data from wikipedia pages
"""
import argparse
import os
from pathlib import Path
import time
import urllib
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

# local (add flag_recognition to your PYTHONPATH)
from common.utils import readfile

# debug
from pprint import pprint  # noqa
import pdb  # noqa


def parse_args():
    """
    parse command-line arguments
    """
    parser = argparse.ArgumentParser()

    cur_file = Path(__file__).absolute()
    default_conf = cur_file.parent / "conf" / (cur_file.stem + ".yml")
    parser.add_argument(
        "--conf",
        default=default_conf,
    )
    return parser.parse_args()


class DownloadFlags:
    """
    Download all data from flag pages. Don't worry about formatting,
    just download it.
    """

    def __init__(self, conf):
        """
        init
        """
        self._driver = None
        self._pages = conf["pages"]
        self._drive_path = conf["chromedriver"]
        self._out_dir = conf["out_dir"]
        self._delay = conf["delay"]

    def __del__(self):
        """
        Always destroy the driver upon exiting
        """
        self._driver.close()

    def initialize_driver(self):
        """
        Initialize the webdriver to be used throughout.
        """
        # these options recommended here
        # https://meta.wikimedia.org/wiki/User-Agent_policy
        opts = Options()
        opts.add_argument("user-agent=bot")
        self._driver = webdriver.Chrome(self._drive_path, chrome_options=opts)

    def download_and_tag_all_images(self):
        """
        This function downloads the full (non-thumbnail) version of all
        images from a given wikipedia website. For flag pages, it will be
        nearly all images of flags, with a few extras (e.g., the wikipedia
        commons logo).
        """
        self.initialize_driver()

        for page in self._pages:
            # There are so many images, this page usually takes a sec to load
            self._driver.get(page)

            images = self._driver.find_elements_by_tag_name("img")
            for image in tqdm(images):
                thumb = image.get_attribute("src")

                # TODO(jafek.ben) is this always how they store them?
                full_size = os.path.dirname(thumb).replace("thumb/", "")
                local_name = os.path.join(
                    self._out_dir,
                    os.path.basename(full_size).replace("%2C_", "+"),
                )
                if os.path.isfile(local_name):
                    continue

                try:
                    urllib.request.urlretrieve(full_size, local_name)
                except urllib.error.HTTPError:
                    print ("did not download:", full_size)

                time.sleep(self._delay)


if __name__ == "__main__":
    args = parse_args()
    conf = readfile(args.conf)
    DF = DownloadFlags(conf)
    DF.download_and_tag_all_images()
