import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lsh-for-indexing",
    author="Ofer Helman",
    version="0.0.5",
    author_email="helmanofer@gmail.com",
    description="Package for indexing vectors to solr/es",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helmanofer/lsh-for-indexing",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "scipy", "scikit-learn"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
