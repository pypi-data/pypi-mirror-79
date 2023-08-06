import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="mango_coding_test_pl_sept20",
    version="2.0.0",
    description="Solutions to Mango's Python Coding Test",
    long_description=README,
    packages=["mango_test"],
    install_requires=["numpy"],
)
