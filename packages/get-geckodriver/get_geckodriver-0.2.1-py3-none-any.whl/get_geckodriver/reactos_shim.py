"""
Experimental support for ReactOS for testing purposes. Mirrors Windows 32-bit execution but on Python 3.4.
"""
import os
import subprocess
import platform
import urllib.request
import urllib.error
import logging
import zipfile

from .errors import *
from io import BytesIO

__author__ = "Yeongbin Jo <yeongbin.jo@pylab.co>, Ka55i0peia and Eadaen <eadaen@protonmail.com>"
# Copyright (c) 2020 Eadaen <eadaen@protonmail.com> GNU AGPL-3.0-or-later.
# Copyright (c) 2020 Ka55i0peia, contributions under MIT Licence.
# Copyright (c) 2019 Yeongbin Jo <yeongbin.jo@pylab.co>, contributions under MIT Licence.
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


class ReactPlatformError(RuntimeError):
    pass


def get_geckodriver_url(version):
    return "https://github.com/mozilla/geckodriver/releases/download/{}/geckodriver-{}-win32.zip".format(
        version, version
    )


def get_platform_architecture():
    pass


def get_firefox_version():
    path1 = "C:\\PROGRA~1\\Mozilla Firefox\\firefox.exe"
    if os.path.exists(path1):
        process = subprocess.Popen([path1, '-v', '|', "more"], stdout=subprocess.PIPE)
    else:
        raise FirefoxNotFoundError
    version = process.communicate()[0].decode("UTF-8").replace("Mozilla Firefox", "").strip()
    return version


def _get_latest_geckodriver_version():
    return "v0.11.0"


def _uncompress(file, directory):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(directory)


def download_geckodriver():
    system = platform.system()
    if system != "Windows":
        raise ReactPlatformError("Platform not supported on Python <= 3.6.")
    get_firefox_version()
    geckodriver_version = _get_latest_geckodriver_version()
    geckodriver_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        geckodriver_version
    )
    geckodriver_filename = "geckodriver.exe"
    geckodriver_filepath = os.path.join(geckodriver_dir, geckodriver_filename)

    if not os.path.isfile(geckodriver_filepath):
        logging.debug(f"Downloading geckodriver ({geckodriver_version})...")
        if not os.path.isdir(geckodriver_dir):
            os.mkdir(geckodriver_dir)
        url = get_geckodriver_url(geckodriver_version)
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            raise urllib.error.URLError("Not Found")
        archive = BytesIO(response.read())

        _uncompress(archive, geckodriver_dir)
    else:
        logging.debug("geckodriver is already installed.")
    if not os.access(geckodriver_filepath, os.X_OK):
        os.chmod(geckodriver_filepath, 0o744)
    return geckodriver_filepath


raise Warning("Python <= 3.6 only supported on ReactOS.")
