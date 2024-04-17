from setuptools import setup, find_packages

setup(
    name='time_aware_graph',
    version='0.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    description='A Time-Aware Graph data structure in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rasheed Salami',
    author_email='amiolas58@gmail.com',
    url='https://github.com/CommanderOutpost/time_aware_graph', 
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license_files=('LICENSE',),
)
