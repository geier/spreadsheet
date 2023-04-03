import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spread",
    version="0.0.1",
    author="Christian Geier",
    author_email="github@lostpackets.de",
    description="Bringing Excel-style formulas to plain text tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geier/spread",
    project_urls={
        "Bug Tracker": "https://github.com/geier/spread/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"spread": "spread"},
    packages=setuptools.find_packages(where="spread"),
    python_requires=">=3.9",
    install_requires=["sly"],
    test_requires=["pytest"],
)
