from setuptools import setup

setup(
    name="marctools",
    version="0.1",
    packages=[""],
    url="",
    license="MIT",
    author="Geoffrey Spear",
    author_email="speargh@pitt.edu",
    description="Command line tools for MARC21 records",
    install_requires=["pymarc", "click"],
    entry_points={
        "console_scripts": [
            "marccount = marctools.marccount:marccount",
            "marcpager = marctools.marcpagerimp:marcpager"
        ]
    },
)
