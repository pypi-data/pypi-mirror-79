import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sweatygoals",
    version='0.2',
    author="Andres Alcocer",
    author_email="andresalcocer7@yahoo.com",
    description="A CLI tool that retrieves latest football matches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndresXI/sweaty-goals",
    packages=setuptools.find_packages(),
)