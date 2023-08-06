import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="AkshayFirstModule",
    version="1.0.0",
    description="It cubes the number",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/uditvashisht/saral-square",
    author="Akshay Dhomse",
    author_email="adhomse99@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["cube"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "cube=cube.__main__:main",
        ]
    },
)
