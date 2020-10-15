import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hotmail-eml-to-text-converter",
    version="0.0.1",
    author="Mike Glover",
    description="Tool to create series of .txt files from hotmail .eml chains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bs4',
    ],
    python_requires='>=3.6',
)