import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvmncards",
    version="0.0.2",
    author="Djeck",
    author_email="work7kost@gmail.com",
    description="Create anki cards and export its in .apkg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djeck1432/anki_deck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)