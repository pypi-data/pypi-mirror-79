"""
This file is used to install this package via the pip tool.

It keeps track of versioning, as well as dependencies and
what versions of python we support.
"""
from setuptools import find_packages, setup


setup(
    name="async-rediscache",
    version="0.1.0-alpha",
    description="An easy to use asynchronous Redis cache",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Python Discord",
    author_email="staff@pythondiscord.com",
    url="https://github.com/SebastiaanZ/async-rediscache",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: AsyncIO",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "aioredis>=1"
    ],
    extras_require={
        "dev": ["flake8", "fakeredis>=1.3.1"],
        "fakeredis": ["fakeredis>=1.3.1"],
    },
    include_package_data=True,
    zip_safe=False
)
