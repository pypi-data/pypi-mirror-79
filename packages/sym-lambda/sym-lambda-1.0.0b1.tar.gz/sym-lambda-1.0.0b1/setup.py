import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sym-lambda",
    version="1.0.0b1",
    author="Sym Inc",
    author_email="info@symops.io",
    description="Sym Lambda Integration Helpers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/symopsio",
    namespace_packages=["sym"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.6",
)
