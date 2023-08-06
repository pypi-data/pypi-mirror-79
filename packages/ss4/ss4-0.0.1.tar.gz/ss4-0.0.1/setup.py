import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ss4",
    version="0.0.1",
    author="Binyamin binni",
    author_email="bnmn6464@gmail.com",
    description="zip executer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/binyamin-binni",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
