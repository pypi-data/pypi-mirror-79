from setuptools import setup, find_packages            # always import that!

setup(
    name="find_couplings",                             # your package's name
    version="0.0.2",                                   # version number
    description="lookup json x vales for jpeg files",  # short description
    scripts=["find_couplings"],
    author="Yogender Pal Chandra",                            # your name
    author_email="yogender027mae@gmail.com",        # your e
    keywords=["json"],                                 # key word for search in pypi
    url="https://YogenderPalChandra@bitbucket.org/YogenderPalChandra/find_couplings_package.git",     # your public repo (here just example)
    packages=find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
