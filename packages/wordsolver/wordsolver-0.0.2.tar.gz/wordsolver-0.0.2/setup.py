from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="wordsolver",
    version="0.0.2",
    author="Christopher Malcolm",
    author_email="chris.c.malcolm.96@gmail.com",
    description="A package to solve word games",
    #long_description_content_type="text/markdown",
    #long_description=long_description,
    url="https://github.com/chrismalcolm/solver",
    packages=["wordsolver"],
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
    install_requires=["numpy>=1.9.3", "pythonds>=1.2.1"]
)
