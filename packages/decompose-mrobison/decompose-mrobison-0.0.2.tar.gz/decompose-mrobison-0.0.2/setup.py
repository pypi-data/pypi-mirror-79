import setuptools

"""
Steps for publishing:
1) increment version number
2) $ python setup.py sdist
3) $ twine upload dist/decompose-mrobison-{version}.tar.gz
"""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="decompose-mrobison",
    version="0.0.2",
    author="Mike Robison",
    author_email="mrobison@wts.edu",
    description="A module for decomposing strings in the latin alphabet to the ascii subset.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wts-dev/decompose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)

#from distutils.core import setup

# To use locally: pip install -e ../populi-api-python/
