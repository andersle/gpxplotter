# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Read a generated map as HTML and take a screenshot."""
import importlib
import io
import pathlib
import sys
import time
import tempfile
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image


def convert(html, thumb, pngfile=None):
    """Convert HTML to a PNG image."""
    dirname = pathlib.Path(__file__).parent
    with tempfile.NamedTemporaryFile(mode='w', dir=dirname) as temp:
        temp.write(html)
        temp.flush()
        url = 'file://' + temp.name

        driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install()
        )
        driver.get(url)
        driver.set_window_position(0, 0)
        driver.set_window_size(400*3, 280*3)
        time.sleep(5)
        result = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(result))
        thumbnail = image.resize((400, 280), Image.ANTIALIAS)
        with open(thumb, 'wb') as output:
            thumbnail.save(output, format='PNG')
        if pngfile is not None:
            driver.save_screenshot(pngfile)
        driver.quit()


def main(pyfiles):
    """Read the given input files and generate pngs."""
    for pyfile in pyfiles:
        libfile = pyfile.split('.py')[0]
        mod = importlib.import_module(libfile)
        html = mod.the_map._repr_html_()
        convert(html, f'sphx_glr_{libfile}_thumb.png')


if __name__ == '__main__':
    main(sys.argv[1:])
