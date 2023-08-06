from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'


]

setup(
    name='ptolemaios',
    version='0.0.1',
    description='basic print func',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Shabix Lampard',
    author_email='charmzshab@gmail.com',
    classifiers=classifiers,
    keywords='',
    license='MIT',
    packages=find_packages(),
    install_requires=['']
)