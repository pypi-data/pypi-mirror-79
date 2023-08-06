from setuptools import setup, find_packages

setup(
    name = "lonny_proc",
    version = "1.2",
    scripts = ["bin/proc"],
    packages = find_packages()
)