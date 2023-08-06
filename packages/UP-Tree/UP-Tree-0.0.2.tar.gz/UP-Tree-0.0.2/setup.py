import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UP-Tree",  # Replace with your own username
    version="0.0.2",
    author="Mithil Ghinaiya",
    author_email="mghinaiya@gmail.com",
    description="This is a simple module which takes input of transactions and provides it's UP-Tree, HeaderTable, and transactions dictionary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miths/UPTree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
