# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Read a generated map as HTML and take a screenshot."""
import io
import os
import pathlib
import runpy
import sys
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.firefox.service import (
    Service as FirefoxService,
)
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image


def convert(html, thumb, pngfile=None):
    """Convert HTML to a PNG image."""
    dirname = pathlib.Path(__file__).parent
    with tempfile.NamedTemporaryFile(
        mode="w", dir=dirname
    ) as temp, tempfile.TemporaryDirectory(
        suffix=".profile", dir=dirname
    ) as profile:
        temp.write(html)
        temp.flush()
        url = f"file://{temp.name}"

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--profile")
        options.add_argument(f"{profile}")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )
        print(f"Loading: {url}")
        driver.get(url)
        print("\t Move/resize...")
        driver.set_window_position(0, 0)
        driver.set_window_size(400 * 3, 280 * 3)
        print("\t Sleep...")
        time.sleep(5)
        print("\t Store png...")
        result = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(result))
        thumbnail = image.resize((400, 280), Image.Resampling.LANCZOS)
        with open(thumb, "wb") as output:
            thumbnail.save(output, format="PNG")
        if pngfile is not None:
            driver.save_screenshot(pngfile)
        driver.quit()


def main(pyfiles):
    """Read the given input files and generate pngs."""
    for pyfile in pyfiles:
        path = pathlib.Path(pyfile).resolve()
        cwd = os.getcwd()
        try:
            print(f"{path.stem}")
            os.chdir(path.parent)
            mod = runpy.run_path(path)
            html = mod["the_map"]._repr_html_()
            convert(html, f"sphx_glr_{path.stem}_thumb.png")
        finally:
            os.chdir(cwd)


if __name__ == "__main__":
    main(sys.argv[1:])
