import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Artists",  # package name
    version="0.0.2",
    author="Jinhwan Kim",
    author_email="jinhwan.kim@codestates.com",
    description="Crawling Package",
    long_description=long_description,  # read from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/jhk0530/artists",  # need to update
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
