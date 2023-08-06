import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cifter", # Replace with your own username
    version="0.0.1",
    author="Simon Rankine",
    author_email="cifter@rankine.me",
    description="An Python3 ATOC file parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simonrankine/cifter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)