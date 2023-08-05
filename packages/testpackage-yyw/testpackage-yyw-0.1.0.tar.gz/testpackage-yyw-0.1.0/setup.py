from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='testpackage-yyw',
    version='0.1.0',
    keywords=('simple', 'test'),
    description='just a simple test',
    license='MIT License',

    author='steve',
    author_email='',

    packages=find_packages(),
    platforms='any',
)