import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sheet-sql-report", # Replace with your own username
    version="0.0.1",
    author="Jack Pegler",
    author_email="jackpegler@gmail.com",
    description="Python package to help users connect with google sheet and SQL data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackpegler/sheet-sql-report",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7.4',
)
