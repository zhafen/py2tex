import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py2tex",
    version="0.1",
    author="Zach Hafen",
    author_email="zachary.h.hafen@gmail.com",
    description= "Tools for saving things in a latex-compatible format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhafen/linefinder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=[
    # ],
    py_modules=[ 'py2tex', 'utilities' ],
)
