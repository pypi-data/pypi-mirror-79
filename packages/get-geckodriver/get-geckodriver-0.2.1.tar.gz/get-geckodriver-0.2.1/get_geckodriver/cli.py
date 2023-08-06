"""
Terminal interface for package.
"""
import argparse
import time
from get_geckodriver import core

__author__ = "Eadaen <eadaen@protonmail.com>"
# Copyright (c) 2020 Eadaen <eadaen@protonmail.com> GNU AGPL-3.0-or-later.
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


def test():
    from selenium import webdriver

    with webdriver.Firefox() as browser:
        browser.get("http://www.pypi.org")
        time.sleep(60)


parser = argparse.ArgumentParser(description="Install geckodriver")
parser.add_argument("-c", dest="force_compile", action="store_true", help="Force compile, even if binary available.")
parser.add_argument("--install-rust", dest="install_rust", action="store_true", help="Automatically install rust.")
parser.add_argument("--remove-rust", dest="remove_rust", action="store_true",
                    help="Automatically uninstall rust if needed to install.")
parser.add_argument("-t", dest="target", help="Specify directory to save geckodriver.")
parser.add_argument("--test", dest="test", action="store_true", help="Test geckodriver. Requires Selenium.")


def main():
    args = parser.parse_args()
    target = args.target if args.target else "auto"
    core.download_geckodriver(target=target, autoinstall_rust=args.install_rust,
                              autoremove_rust=args.remove_rust, force_compile=args.force_compile)
    if args.test:
        test()


if __name__ == "__main__":
    main()
