import re
from codecs import open
from os import path

from setuptools import setup, find_packages

with open("gradient_utils/__init__.py", "r", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "wheel",
    "numpy<1.19",    # 1.18 is last stable version that works on Py3.5
    "hyperopt<0.2",  # hyperopt==0.2 does not work on Py<3.6
    "pymongo",
    "prometheus_client",
]

dev_requirements = [
    "tox",
    "mock",
]

setup(
    name="gradient_utils",
    version=version,
    description="Gradient Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Paperspace/gradient-utils",
    author="Paperspace Co.",
    author_email="info@paperspace.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="gradient utils sdk",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements
    }
)
