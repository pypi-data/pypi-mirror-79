import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distrib_sample", 
    version="0.0.1",
    author="Clar Ni Shealbhaigh",
    author_email="author@example.com",
    description="Package to draw random samples",
    long_description=long_description,
    long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)



