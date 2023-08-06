import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="luangpor", 
    version="0.0.2",
    author="Korakot Chaovavanich",
    author_email="korakot@gmail.com",
    description="Access Luangpor Pramote's talks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/korakot/luangpor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
