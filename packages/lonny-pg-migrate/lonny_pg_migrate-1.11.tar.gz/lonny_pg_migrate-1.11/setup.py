from setuptools import setup, find_packages

setup(
    name = "lonny_pg_migrate",
    version = "1.11",
    packages = find_packages(),
    scripts = [ "bin/pg_migrate"]
)