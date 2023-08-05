import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="print-dot-salamtam",
    version="0.0.2",
    author="salamtam",
    author_email="salamtam.p@gmail.com",
    description="print dot for test the coding work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salamtamp/print-dot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
