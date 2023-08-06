import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="complete", 
    version="0.0.1",
    author="DankCoder",
    author_email="business.dankcoder@gmail.com",
    description="A Python library to autocomplete questions using search engines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["aiohttp","requests", "lxml"],
    include_package_data=True
)
