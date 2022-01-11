from setuptools import setup, find_packages

VERSION="0.0.6a"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="log12",
    version=VERSION,
    url='https://github.com/nkratzke/log12',
    license='MIT',
    author='Nane Kratzke',
    author_email='nane.kratzke@th-luebeck.de',
    description='Logging for 12-factor apps.',
    long_description_content_type="text/markdown",
    long_description=long_description,
    python_requires=">=3.7,<4.0",
    install_requires=[
          'nanoid',
          'msgpack'
    ],
    packages=find_packages()
)