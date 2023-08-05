import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythematics",
    version="2.0.0",
    author="Greece4ever",
    author_email="programertv633@gmail.com",
    description="Python Math library for Matrix and Polynomial manipulation extending to the complex plane",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Greece4ever/pythematics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
