from setuptools import setup


__author__ = "Eadaen <eadaen@protonmail.com>"


with open("README.md") as readme_file:
    long_description = readme_file.read()


setup(
    name="get-geckodriver",
    version="0.2.1",
    author="Eadaen",
    author_email="eadaen@protonmail.com",
    description="Automatically install geckodriver, compile if required.",
    license="GNU AGPL-3.0-or-later",
    keywords="geckodriver selenium splinter",
    url="https://codeberg.org/Eadaen1/get-geckodriver",
    packages=["get_geckodriver"],
    long_description_content_type="text/markdown",
    long_description=long_description,
    entry_points={
        "console_scripts": [
            "get-geckodriver = get_geckodriver.cli:main"
        ]
    },
    python_requires=">=3.4",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Installation/Setup",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows ",
        "Operating System :: POSIX :: BSD",
        "Operating System :: Unix",
        "Operating System :: Other OS",
        "Operating System :: Android"
    ],
)
