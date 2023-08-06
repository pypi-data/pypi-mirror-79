#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='authlib-httpx',
    version='0.1.1',
    author='Ber Zoidberg',
    author_email='ber.zoidberg@gmail.com',
    url='http://authlib.org',
    packages=find_packages(include=('authlib_httpx',)),
    description=(
        'Temporary location of full httpx support until authlib merges this upstream'
    ),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    long_description=readme,
    license='BSD-3-Clause',
    install_requires=['httpx'],
    project_urls={
        'Documentation': 'https://docs.authlib.org/',
        'Commercial License': 'https://authlib.org/plans',
        'Bug Tracker': 'https://github.com/lepture/authlib/issues',
        'Source Code': 'https://github.com/lepture/authlib',
        'Blog': 'https://blog.authlib.org/',
        'Donate': 'https://lepture.com/donate',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
