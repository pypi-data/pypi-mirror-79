import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stockie", 
    version="0.0.3",
    author="Suparjo Tamin",
    author_email="suparjo.tamin@gmail.com",
    description="A package to identify stock candlestick pattern",
    long_description=long_description,
    url="https://github.com/suparjotamin/stocky",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
