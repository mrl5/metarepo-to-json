import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="metarepo2json",
    version="1.0.0-SNAPSHOT",
    author="mrl5",
    description="Funtoo meta-repo to JSON exporter",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mrl5/metarepo-to-json",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    install_requires=["pop>=12", "aiohttp>=3.6.2", "GitPython>=3.1.1"],
    packages=setuptools.find_packages(),
)
