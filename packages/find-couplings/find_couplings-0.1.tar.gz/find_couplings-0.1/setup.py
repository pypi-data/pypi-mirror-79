#from setuptools import setup, find_packages            # always import that!

from setuptools import setup
import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='find_couplings',
      version='0.1',
      description='lookup x coordinates for couplings in jpeg files',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Visualization'
      ],
      keywords='list of Pandas series to list of pandas data frame',
      url='https://YogenderPalChandra@bitbucket.org/YogenderPalChandra/find_couplings.git',
      author='Yogender Pal Chandra',
      python_requires=">=3.6",
      author_email='yogender027mae@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False)
