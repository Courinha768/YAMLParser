from setuptools import setup, find_packages

setup(
    name="yaml",
    version="0.5",
    packages=find_packages(where="sources"),
    package_dir={"": "sources"},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
