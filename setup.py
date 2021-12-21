from setuptools import setup, find_packages
import log12

VERSION="0.0.1rc3"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="log12",
    version=VERSION,
    url='https://github.com/nkratzke/log12',
    license='MIT',
    author='Nane Kratzke',
    author_email='nane.kratzke@th-luebeck.de',
    description='Structured logging, the 12-factor style.',
    long_description_content_type="text/markdown",
    long_description=long_description,
    python_requires=">=3.6,<4.0",
    packages=find_packages()
)