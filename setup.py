from setuptools import setup, find_packages

setup(
    name="py-watcher",
    version="0.1.0",
    description="Py-Watcher is a CLI tool that watches for changes in your code and runs pytest on the changed files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Deviljin112",
    url="https://github.com/deviljin112",
    license="MIT",
    keywords="python pytest testing testing-tools watch watcher",
    packages=find_packages(include=["src"]),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={"console_scripts": ["pytest-w=src.main:cli"]},
    setup_requires=["pytest-runner", "black"],
    tests_require=["pytest"],
)
