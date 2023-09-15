from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dictor",
    version="0.1.12",
    description="an elegant dictionary and JSON handler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perfecto25/dictor",
    author="mike.reider",
    author_email="mike.reider@gmail.com",
    license="MIT",
    packages=["dictor"],
    zip_safe=True,
)
