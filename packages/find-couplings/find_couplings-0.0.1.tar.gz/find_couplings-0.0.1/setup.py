from setuptools import setup, find_packages            # always import that!

setup(
    name="find_couplings",                             # your package's name
    version="0.0.1",                                   # version number
    description="lookup json x vales for jpeg files",  # short description
    scripts=["find_couplings"],
    author="Gwang-Jin Kim",                            # your name
    author_email="gwang.jin.kim.phd@gmail.com",        # your e
    keywords=["json"],                                 # key word for search in pypi
    url="https://bitbucket.org/gwangjinkim/find_couplings_pkg",     # your public repo (here just example)
    packages=find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
