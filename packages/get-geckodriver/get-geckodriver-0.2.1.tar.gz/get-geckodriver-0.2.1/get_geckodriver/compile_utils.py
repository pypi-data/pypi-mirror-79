"""
Helper functions for compiling geckodriver.
"""
import os
import subprocess
import logging
from .errors import *

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


def detect_freebsd_linux_compatibility(arch: str) -> bool:
    """
    Checks whether FreeBSD has the required kernel modules for binary compatibility with Linux.
    :param arch: x86 family cpu architecture
    :return: whether the modules are available and enabled
    """
    kernel_module = "linux.ko" if arch == "32" else "linux64.ko"
    #  todo do checks as in https://www.freebsd.org/doc/handbook/linuxemu.html

    with subprocess.Popen("/usr/local/bin/ksh93", stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
        output = proc.communicate("kldstat".encode("utf8"))[0]
        return kernel_module in output.decode("utf8")


def _is_cargo_installed() -> bool:
    """
    Check whether cargo is installed.
    :return: whether cargo is installed
    """
    return os.path.exists("$HOME/.cargo/env")


def _has_shell(s: str) -> bool:
    """
    Checks if a particular shell exists in /bin on the system.
    :param s: Name of shell.
    :return: True if s is in /bin
    """
    return os.path.exists(f"/bin/{s}")


def _get_shell(platform: str) -> str:
    """
    Find the bash-like shell available on the operating system.
    :param platform: Operating system type.
    :return:
    """
    if platform == "linux": # todo experiment with xonsh
        for sh in ["bash", "zsh", "crosh", "dash", "fish"]:  # todo check that fish can parse the file
            if _has_shell(sh):
                return f"/bin/{sh}"  # todo make this /usr/bin/env {sh} for portability; check this works
        ts = "/data/data/com.termux/files/usr/bin/bash"
        if os.path.exists(ts):
            return ts
        else:
            raise PlatformError("Compatible shell not found on system.")
    elif platform == "bsd":
        return "/usr/local/bin/ksh93"
    else:
        raise NotImplementedError


# todo figure out target
def compile_geckodriver(geckodriver_dir: str, version: str, platform: str, target: str,
                        autoinstall_rust=True, autoremove_rust=False) -> str:
    """
    Builds geckodriver from source.
    :param geckodriver_dir: path to directory for installation
    :param version: geckodriver version
    :param platform: Operating system type.
    :param autoinstall_rust: automatically install rustc
    :param autoremove_rust: automatically remove rustc when no longer needed
    :param target: Path to save geckodriver binary
    :return: path of binary
    """
    if not autoinstall_rust:
        autoremove_rust = False

    logging.log(20, "Compiling...")
    source_filepath = os.path.join(geckodriver_dir, f"geckodriver{version.replace('v', '-')}")
    cwd_old = os.getcwd()
    os.chdir(source_filepath)

    if autoinstall_rust:
        if not _is_cargo_installed():
            rust_installer = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > /tmp/rustup.sh"
            os.system(rust_installer)
            os.system("sh rustup.sh -y")

    shell = _get_shell(platform)
    logging.log(20, "Compiling ...")
    compile_command = "source $HOME/.cargo/env; cargo build --release"
    with subprocess.Popen(shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
        output = proc.communicate(compile_command.encode("utf8"))[0]
        logging.log(10, output.decode("utf8"))
    logging.log(20, "Compiled")

    if autoremove_rust:
        os.system("rustup self uninstall -y")

    os.chdir(cwd_old)
    return os.path.join(source_filepath, f"target/release/geckodriver")
