import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raise_assert",
    version="0.1",
    author="Jean Rabault",
    author_email="jean.rblt@gmail.com",
    description="an alternative to assert - guaranteed to raise",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jerabaul29/raise_assert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
