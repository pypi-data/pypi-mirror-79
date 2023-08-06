#import setuptools
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="SmileValidation",
    version="1.1.0",
    author="Sitthykun LY",
    author_email="ly.sitthykun@gmail.com",
    description="Python3 Validation in another way",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/sitthykun/smilevalidation",
    packages=["smilevalidation","smilevalidation/rule","smilevalidation/schema"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
