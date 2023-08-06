import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssb-pkg",
    version="0.1.0",
    author="Chris De Leon",
    author_email="chrisdeleon333@gmail.com",
    description="A package for detecting and visualizing sinks, sources, and bridges in networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chipdelmal.github.io/MoNeT/SSBSTP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    python_requires='>=3.6',
)