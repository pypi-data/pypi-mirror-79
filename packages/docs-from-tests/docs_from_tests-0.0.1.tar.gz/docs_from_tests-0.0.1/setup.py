import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docs_from_tests",
    version="0.0.1",
    author="RES",
    author_email="cedd.burge@res-group.com",
    description="A short description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/resgroup/docs-from-tests",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[],
)
