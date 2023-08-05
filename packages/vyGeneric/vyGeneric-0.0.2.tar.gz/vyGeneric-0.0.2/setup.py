import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vyGeneric",
    version="0.0.2",
    author="Nitesh Bhandari",
    #author_email="nitesh@vayavya.co.in",
    description="Package for creating generic objects with transparent 'repr'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niteshb/common-python-vyGeneric",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
