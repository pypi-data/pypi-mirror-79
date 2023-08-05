from distutils.core import setup

from setuptools import find_packages

try:
    with open("./README.md", "r") as f:
        file: str = f.read()
except FileNotFoundError:
    print("[ERROR] Can't find README.md")
    file: str = "Russel-Python-Interface"

setup(
    name="russel-python-interface",
    packages=find_packages(),
    version="v0.1a6",
    license="GPL-2.0",
    description="Russel communication wrapper allows easier integration into other projects.",
    author="revol-xut",
    author_email="revol-xut@protonmail.com",
    long_description_content_type="text/markdown",
    long_description=file,
    url="https://bitbucket.org/revol-xut/russel-python-interface/",
    keywords=["russel", "cluster", "communication wrapper"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
