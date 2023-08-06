"""

    ###################
    ##               ##
    ##    Pi-Clap    ##
    ##               ##
    ###################

Repo: https://github.com/nikhiljohn10/pi-clap
Author: Nikhil John
License: MIT
"""
from piclap import __version__ as VERSION

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pi-clap",
    version=VERSION,
    author="Nikhil John",
    author_email="ceo@jwala.diamonds",
    description="A python package for clap detection",
    url="https://pi-clap.nikz.in",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/nikhiljohn10/pi-clap",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        'Environment :: Console',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    platforms="any",
    py_modules=['piclap'],
    python_requires='>=3.6',
    install_requires=[
        "gpiozero==1.5.1",
        "pyaudio==0.2.11",
        "munch==2.5.0",
    ],
)
