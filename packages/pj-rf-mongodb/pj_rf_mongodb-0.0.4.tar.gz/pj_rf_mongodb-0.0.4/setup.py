import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pj_rf_mongodb",
    version="0.0.4",
    description="Get Data from MongoDB during execution using Robot Framework..",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    author="PJ Gevana",
    author_email="patdroidz@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pj_rf_mongodb"],
    include_package_data=True,
    # install_requires=["requests"],
)
