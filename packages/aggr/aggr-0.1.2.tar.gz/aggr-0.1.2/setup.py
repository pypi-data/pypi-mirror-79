from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aggr",
    version="0.1.2",
    author="François-Xavier Devailly, Xinyue Tan",
    author_email='francois-xavier.devailly@hec.ca, xinyue.tan@hec.ca',
    packages=['aggregator','aggregator.GCN'],
    url="https://github.com/Daahorst/Aggregator",
    description="Automate feature aggregation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT'
    )
