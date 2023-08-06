from setuptools import setup, find_packages

setup(
    name = "lonny_pg_cron",
    version = "1.8",
    packages = find_packages(),
    scripts = ["bin/pg_cron"]
)