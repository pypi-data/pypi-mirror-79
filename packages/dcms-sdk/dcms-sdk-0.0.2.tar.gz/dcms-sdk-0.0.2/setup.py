import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dcms-sdk",
    version="0.0.2",
    author="easson",
    author_email="qhzhyt@163.com",
    description="the sdk of data crawl manage system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qhzhyt/dcms-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
