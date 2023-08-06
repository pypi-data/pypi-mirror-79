"""
Helper functions for filename and URL generation.
"""
import os
import sys
import platform
import subprocess
import shutil
import urllib.request
import urllib.error
from pathlib import Path
import logging
import tarfile
import zipfile

from .compile_utils import compile_geckodriver, detect_freebsd_linux_compatibility
from io import BytesIO
from .errors import *

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

_PLATFORM, _ARCHITECTURE, _COMPRESSION = "", "", ""


def _get_geckodriver_filename() -> str:
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if _PLATFORM == "win":
        return "geckodriver.exe"
    return "geckodriver"


def get_platform_architecture() -> None:
    """
    Finds the operating system and processor architecture.
    :return: None
    """
    global _PLATFORM, _ARCHITECTURE, _COMPRESSION

    x86_64 = {"x86_64", "amd64", "AMD64", "64bit"}
    i386 = {"i386", "i486", "i586", "i686", "386", "x86", "32bit"}

    system = platform.system()
    if system == "Windows":
        machine = platform.machine()
    else:
        machine = os.uname().machine

    if system == "Linux":
        _PLATFORM = "linux"
        if machine in x86_64:
            _ARCHITECTURE = "64"
        elif machine in i386:
            _ARCHITECTURE = "32"
        else:
            _ARCHITECTURE = "other"

    elif system in {"OpenBSD", "NetBSD", "FreeBSD"}:
        _PLATFORM = "bsd"
        _ARCHITECTURE = "other"
        if system == "FreeBSD":
            if machine in x86_64:
                if detect_freebsd_linux_compatibility("64"):
                    _PLATFORM = "linux"
                    _ARCHITECTURE = "64"
            elif machine in i386:
                if detect_freebsd_linux_compatibility("32"):
                    _PLATFORM = "linux"
                    _ARCHITECTURE = "32"

    elif system in {"Haiku", "Hurd"}:
        _PLATFORM = "linux"
        _ARCHITECTURE = "other"

    elif system == "Darwin":
        _PLATFORM = "mac"
        _ARCHITECTURE = "os"
    elif system == "Windows":
        _PLATFORM = "win"
        if machine in x86_64:
            _ARCHITECTURE = "64"
        elif machine in i386:
            _ARCHITECTURE = "32"
    if not all([_PLATFORM, _ARCHITECTURE]):
        raise PlatformError(f"Failed to detect appropriate platform. {system} {machine}")

    if _PLATFORM == "win":
        _COMPRESSION = "zip"
    else:
        _COMPRESSION = "tar.gz"


def get_geckodriver_url(version: str) -> str:
    """
    Generates the download URL for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.
    :param version: the version of geckodriver
    :return: Download URL for geckodriver
    """
    if _ARCHITECTURE == "other":  # or platform BSD
        return f"https://github.com/mozilla/geckodriver/archive/{version}.{_COMPRESSION}"
    else:
        return f"https://github.com/mozilla/geckodriver/releases/download/{version}" \
               f"/geckodriver-{version}-{_PLATFORM}{_ARCHITECTURE}.{_COMPRESSION}"


def find_binary_in_path(filename: str) -> str:
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path
    """
    if "PATH" not in os.environ:
        raise PATHNotFoundError
    for directory in os.environ["PATH"].split(os.pathsep):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    raise BinaryNotFoundError


def get_firefox_version() -> str:
    """
    :return: the version of firefox installed on client
    """
    if _PLATFORM == "linux":
        with subprocess.Popen(['firefox', "--version"], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode("utf-8").replace("Mozilla Firefox", "").strip()
    elif _PLATFORM == "mac":
        process = subprocess.Popen(
            ["/Applications/Firefox.app/Contents/MacOS/firefox", "--version"], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode("UTF-8").replace("Mozilla Firefox", "").strip()
    elif _PLATFORM == "win":
        path1 = "C:\\PROGRA~1\\Mozilla Firefox\\firefox.exe"
        path2 = "C:\\PROGRA~2\\Mozilla Firefox\\firefox.exe"
        if os.path.exists(path1):
            process = subprocess.Popen([path1, '-v', '|', "more"], stdout=subprocess.PIPE)
        elif os.path.exists(path2):
            process = subprocess.Popen([path2, '-v', '|', "more"], stdout=subprocess.PIPE)
        else:
            raise FirefoxNotFoundError
        version = process.communicate()[0].decode("UTF-8").replace("Mozilla Firefox", "").strip()
    else:
        raise NotImplementedError
    return version


def _get_major_version(version: str) -> str:
    """
    :param version: the version of firefox
    :return: the major version of firefox
    """
    return version.split('.')[0]


def _get_latest_geckodriver_version() -> str:
    """
    :return: the latest version of geckodriver
    """
    url = urllib.request.urlopen("https://github.com/mozilla/geckodriver/releases/latest").geturl()
    if "/tag/" not in url:
        raise GeckodriverVersionNotFoundError
    return url.split('/')[-1]


def get_geckodriver_path() -> str:
    """
    :return: path of the geckodriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def download_geckodriver(target="auto", autoinstall_rust=True, autoremove_rust=False,
                         force_compile=False) -> str:
    """
    Downloads, unzips and installs geckodriver.
    If a geckodriver binary is found in PATH it will be copied, otherwise downloaded.

    :param target: Flag indicating where to download. Path, "auto" or "cwd". Auto redirects to $HOME/bin, cwd to cwd
    :param autoinstall_rust:
    :param autoremove_rust:
    :param force_compile: build geckodriver, even if binary available for system
    :return: The file path of geckodriver
    """
    global _ARCHITECTURE
    if force_compile:
        _ARCHITECTURE = "other"
        if _PLATFORM in {"win", "mac"}:
            raise NotImplementedError

    if target.lower() == "cwd":
        target = os.getcwd()
    elif target.lower() == "auto":
        target = f"{str(Path.home())}/bin"

    if not os.path.exists(target):
        os.mkdir(target)
    elif not os.path.isdir(target):
        raise NotImplementedError

    get_firefox_version()
    geckodriver_version = _get_latest_geckodriver_version()
    geckodriver_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        geckodriver_version
    )
    print(f"geckodriver_dir: {geckodriver_dir}")
    geckodriver_filename = _get_geckodriver_filename()
    old_geckodriver_filepath = os.path.join(geckodriver_dir, geckodriver_filename)
    binary_path = os.path.join(target, geckodriver_filename)
    if os.path.exists(binary_path):
        return binary_path

    if not os.path.isfile(binary_path):
        logging.log(20, f"Downloading geckodriver ({geckodriver_version})...")
        if not os.path.isdir(geckodriver_dir):
            os.mkdir(geckodriver_dir)
        url = get_geckodriver_url(geckodriver_version)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError("Not Found")
        except urllib.error.URLError:
            raise RuntimeError(f"Failed to download geckodriver archive: {url}")
        archive = BytesIO(response.read())

        _uncompress(archive, geckodriver_dir)
    elif os.path.isdir(binary_path):
        raise NotImplementedError
    else:
        logging.log(20, "geckodriver is already installed.")

    if _ARCHITECTURE == "other":
        old_geckodriver_filepath = compile_geckodriver(geckodriver_dir, geckodriver_version, _PLATFORM, target,
                                                       autoinstall_rust=autoinstall_rust,
                                                       autoremove_rust=autoremove_rust)
    os.rename(old_geckodriver_filepath, binary_path)
    shutil.rmtree(geckodriver_dir, ignore_errors=True)
    if not os.access(binary_path, os.X_OK):
        os.chmod(binary_path, 0o744)
    if not os.access(binary_path, os.X_OK):
        raise Warning("Binary not executable.")
    return binary_path


def _uncompress(file: BytesIO, directory: str) -> None:
    if _COMPRESSION == "zip":
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(directory)
    else:
        tar = tarfile.open(fileobj=file, mode="r:gz")
        tar.extractall(directory)
        tar.close()


get_platform_architecture()


if __name__ == "__main__":
    print(get_firefox_version())
    print(download_geckodriver())
