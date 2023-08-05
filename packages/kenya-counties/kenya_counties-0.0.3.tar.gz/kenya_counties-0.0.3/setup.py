import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kenya_counties",
    version="0.0.3",
    author="John Maluki",
    author_email="johnmaluki58@gmail.com",
    description="This package returns all kenya counties in list and the number of the counties",
    long_description=long_description,
    package_data={'k_counties': ['kenya_counties.txt']},
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://github.com/john-maluki/kenyan_counties",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)