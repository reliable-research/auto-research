from setuptools import setup, find_packages

setup(
    name="autoresearch-codeless",
    version="4.0.0",
    packages=find_packages(include=["autoresearch*"]),
    entry_points={
        "console_scripts": [
            "autoresearch=autoresearch.cli.main:main",
            "idea2paper=autoresearch.cli.main:main",
        ],
    },
)
