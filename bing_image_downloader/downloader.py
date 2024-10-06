import re
import os, sys
import shutil
from pathlib import Path

try:
    from bing import Bing
except ImportError:  # Python 3
    from .bing import Bing


def download(query, limit=100, output_dir='dataset', sub_dir=None, adult_filter_off=True, 
force_replace=False, timeout=60, filter="", verbose=True):

    # engine = 'bing'
    if adult_filter_off:
        adult = 'off'
    else:
        adult = 'on'
    # remove space and special characters in query
    # if sub_dir:
    #     sub_dir = re.sub(r'[\\/*?:"<>|]', '', query).replace(' ', '_')
    image_dir = Path(output_dir).joinpath(sub_dir).absolute()

    if force_replace:
        if Path.is_dir(image_dir):
            shutil.rmtree(image_dir)

    # check directory and create if necessary
    try:
        if not Path.is_dir(image_dir):
            Path.mkdir(image_dir, parents=True)

    except Exception as e:
        # print('[Error]Failed to create directory.', e)
        sys.exit(1)
        
    # # print("[%] Downloading Images to {}".format(str(image_dir.absolute())))
    bing = Bing(query, limit, image_dir, adult, timeout, filter, verbose)
    downloaded_image_paths = bing.run()
    # # print(f"[%] Downloaded {len(downloaded_image_paths)} images to {str(image_dir.absolute())}")
    # for image_path in downloaded_image_paths:
    #     # print(f"[%] {image_path}")
    return downloaded_image_paths


if __name__ == '__main__':
    download('dog', output_dir="..\\Users\\cat", limit=10, timeout=1)
