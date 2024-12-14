from setuptools import setup, find_packages
from fluentflet.__version__ import VERSION

setup(
    name="fluentflet",
    version=VERSION,
    description="Fluent Design System components for Flet",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Edoardo Balducci",
    author_email="edoardoba2004@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "flet[all]>=0.25.2",
    ],
    project_urls={
        "Homepage": "https://github.com/Bbalduzz/fluentflet",
        "Issues": "https://github.com/Bbalduzz/fluentflet/issues",
    },
)
