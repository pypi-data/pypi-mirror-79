from setuptools import setup, find_packages

from version import __version__

setup(name='statisfaction',
      version=__version__,
      description='A library to unify statistical testing at BlaBlaCar',
      keywords='statistics hypothesis test testing',
      author='BlaBlaCar Intelligence Team',
      author_email='adrien.tordjeman@blablacar.com',
      install_requires=[
          'pandas',
          'vertica-python',
          'numpy',
          'scipy',
          'statsmodels'
      ],
      packages=find_packages(),
      test_suite='tests',
      tests_require=['nose-cover3', 'nose'],
      setup_requires=['nose>=1.0'],
      include_package_data=True,
      zip_safe=False)
