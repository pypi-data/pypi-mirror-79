import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdat_analyzer_tmp", # Replace with your own username
    version="0.0.1",
    author="Ani Chattaraj",
    author_email="chattaraj@uchc.edu",
    description="Compute observable averages for BNGL/NFsim model outputs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)