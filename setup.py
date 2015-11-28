#try:
#    from setuptools import setup
#except ImportError:
#    from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name='thlib',
    version='0.0.1dev',
    author='Chia-Chi Chang, Wei-Chih Lin',
    author_email='c3h3.tw@gmail.com, hawkerylin@gmail.com',
    packages=find_packages(),
    install_requires=["html5lib",
                      "requests",
                      "pyquery"],
)
