from setuptools import setup, find_packages

with open("requirements.in") as f:
    setup(
        name = "lonny_pg_worker",
        version = "1.0",
        packages = find_packages(),
        install_requires = f.read().splitlines(),
        scripts = ["bin/pg_job"]
    )