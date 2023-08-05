# encoding: utf-8
from setuptools import setup

def readme():
    """Import README for use as long_description."""
    with open("README.rst") as f:
        return f.read()

version = "0.1.1"

setup(
    name="viltolyckor_scraper",
    version=version,
    description="A scraper of statistical data from viltolyckor.se, built on top of Statscraper.",
    long_description=readme(),
    url="https://github.com/jplusplus/viltolyckor_scraper",
    author="Jens Finnäs",
    author_email="jens.finnas@gmail.com",
    license="MIT",
    packages=["viltolyckor"],
    zip_safe=False,
    install_requires=[
        "statscraper",
        "requests",
        "beautifulsoup4",
        "lxml",
    ],
    test_suite="nose.collector",
    tests_require=["nose"],
    include_package_data=True,
    download_url="https://github.com/jplusplus/viltolyckor_scraper/archive/%s.tar.gz"
                 % version,
)
