import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="metarepo2json",
    version="1.1.0",
    author="mrl5",
    description="Funtoo meta-repo to JSON exporter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrl5/metarepo-to-json",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    install_requires=["pop>=12", "aiohttp>=3.6.2", "GitPython>=3.1.1"],
    packages=setuptools.find_packages(),
)
