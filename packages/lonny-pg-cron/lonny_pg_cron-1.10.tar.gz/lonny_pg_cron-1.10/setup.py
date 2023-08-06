from setuptools import setup, find_packages

setup(
    name = "lonny_pg_cron",
    version = "1.10",
    packages = find_packages(),
    scripts = ["bin/pg_cron"]
)