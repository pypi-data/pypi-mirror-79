import setuptools

with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "xml2ajson",
    version = "0.0.2",
    author = "Mr.Wu",
    author_email = "1160949893@qq.com",
    description = "transfrom the xml files to a json",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
    ],
)