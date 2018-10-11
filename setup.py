import setuptools

with open("README.md", "r") as f:
    longDescription = f.read()

setuptools.setup(
    name="fBrowser",
    version="0.1",
    author="Abe Malla",
    author_email="",
    description="A small example package",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://github.com/FastestMolasses/fBrowser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
