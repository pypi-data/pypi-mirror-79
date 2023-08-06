import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read()

setuptools.setup(
    name="insyde",
    version="0.0.1",
    description="GUI wrapper for static code analysis and visualization tools.",
    author="roschly",
    author_email="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["insyde"],
    install_requires=requirements,
    license="MIT",
    python_requires='>=3.6',
)