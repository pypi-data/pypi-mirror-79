import os
import logging
import sys
from pathlib import Path
if sys.version_info < (3, 6):
    from get_geckodriver import reactos_shim as core
else:
    from get_geckodriver import core
# Copyright (c) 2020 Eadaen <eadaen@protonmail.com> GNU AGPL-3.0-or-later.
# Copyright (c) 2019 Yeongbin Jo <yeongbin.jo@pylab.co>, contributions under MIT License.
"""
    This file is part of get-geckodriver.

    get-geckodriver is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    get-geckodriver is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with get-geckodriver.  If not, see <https://www.gnu.org/licenses/>.
"""


def install(*args, **kwargs):
    """
    Appends the directory of the geckodriver binary file to PATH.

    :return: None
    """
    geckodriver_filepath = core.download_geckodriver(*args, **kwargs)
    if not geckodriver_filepath:
        raise RuntimeError("Could not download geckodriver.")
    geckodriver_dir = os.path.dirname(geckodriver_filepath)
    if 'PATH' not in os.environ:
        os.environ['PATH'] = geckodriver_dir
    elif geckodriver_dir not in os.environ['PATH']:
        os.environ['PATH'] = geckodriver_dir + os.pathsep + os.environ['PATH']


def get_firefox_version():
    """
    Get installed version of Firefox on client

    :return: The version of Firefox
    """
    return core.get_firefox_version()
