import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nopi", # Replace with your own username
    version="0.0.1",
    author="Michael Watson",
    author_email="",
    description="New Orleans Programming Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/M-Watson/nopi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
