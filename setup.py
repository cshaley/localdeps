from os import path
from setuptools import find_packages, setup


# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()


setup(
    name='localdeps',
    packages=find_packages(),
#    package_dir={'src/': 'conda-dev'},
    version="0.0.2",
    description="Install conda package dependencies into a conda environment",
    license="MIT License",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/cshaley/localdeps",
    python_requires=">=3.4",
    include_package_data=True,
    install_requires=[],
    author="@cshaley on github",
    entry_points={"console_scripts": ["localdeps = localdeps:main"]},
    keywords="package dependency local development",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
