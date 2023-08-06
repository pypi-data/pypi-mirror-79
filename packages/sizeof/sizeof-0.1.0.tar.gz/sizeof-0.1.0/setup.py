from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sizeof",
    version="0.1.0",
    packages=["sizeof",],
    install_requires=[],
    license="MIT",
    url="https://github.com/lapets/sizeof",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Simple function for measuring the size in memory "+\
                "of common Python data structures.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
