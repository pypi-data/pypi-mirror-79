""" setup.py """
import setuptools

with open("README.md") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="torchinfo",
    version="0.0.1",
    author="Tyler Yep @tyleryep",
    author_email="tyep@cs.stanford.edu",
    description="Pytorch Info",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/tyleryep/torchinfo",
    packages=["torchinfo"],
    keywords="torch torchinfo",
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
