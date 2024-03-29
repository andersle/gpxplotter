# Copyright (c) 2020, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""Version information for gpxplotter.

This file is generated by gpxplotter (``setup_version.py``).
"""
SHORT_VERSION = "0.2.11"
VERSION = "0.2.11"
FULL_VERSION = "0.2.11"
GIT_REVISION = "c39bdcfda442ab33e94e3737cbc64603b063d531"
GIT_VERSION = "0.2.11"
RELEASE = True

if not RELEASE:
    VERSION = GIT_VERSION
