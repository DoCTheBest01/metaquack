from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="metaquack",
    version="0.1.0",
    author="Alireza Abedini",
    author_email="alirezaabedini520@gmail.com",
    description="MetaQuack: Evolutionary optimization pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/metaquack",
    packages=find_packages(),
    package_data={
        "metaquack": ["lib/ga/*.py"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy==1.26.4",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8", "jupyter", "twine", "build"],
        "notebook": ["jupyter", "matplotlib", "seaborn"],
    },
)