from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt", "r") as req_file:
        return req_file.read().splitlines()

setup(
    name="playlist_operations",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    author="Noah Kupinsky",
    description="A basic Python package for Spotify interactions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/noahkupinsky/PlaylistOperations",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)