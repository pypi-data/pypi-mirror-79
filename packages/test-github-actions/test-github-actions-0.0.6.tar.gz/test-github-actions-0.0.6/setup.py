import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test-github-actions",
    version="0.0.6",
    author="M Sleigh",
    author_email="author@example.com",
    description="Learn/test GitHub Actions for running CI/CD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msleigh/test-github-actions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
