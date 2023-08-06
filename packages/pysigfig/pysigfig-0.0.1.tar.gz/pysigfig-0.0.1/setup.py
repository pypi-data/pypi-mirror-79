from pathlib import Path

import setuptools

project_dir = Path(__file__).parent

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysigfig",
    version="0.0.1",
    author="Rob Carnell",
    author_email="bertcarnell@gmail.com",
    description="A package for creating and manipulating floating point numbers accounting for significant figures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bertcarnell/pysigfig",
    packages=setuptools.find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords=["python", "significant", "chemistry", "physics"],
    package_dir={"": "src"},
    include_package_data=True,
    # This is a trick to avoid duplicating dependencies between both setup.py and
    # requirements.txt.
    # requirements.txt must be included in MANIFEST.in for this to work.
    # It does not work for all types of dependencies (e.g. VCS dependencies).
    # For VCS dependencies, use pip >= 19 and the PEP 508 syntax.
    #   Example: 'requests @ git+https://github.com/requests/requests.git@branch_or_tag'
    #   See: https://github.com/pypa/pip/issues/6162
    install_requires=project_dir.joinpath("requirements.txt").read_text().split("\n"),
    zip_safe=False,
    license="MIT",
    license_files=["LICENSE"],
)
