import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='htnb_getpath',
    version='0.1',
    # scripts=['pypi1'],
    author="Huu Nghia",
    author_email="nghiahtnb@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
