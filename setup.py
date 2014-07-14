# coding: utf-8
"""
:copyright: 2014 Bilal Syed Hussain
:license: Apache 2.0
"""

import sys
import gmusicSyncRatings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('Readme.md') as f:
        return f.read()

def requirements():
    install_requires = []
    with open('requirements.txt') as f:
        for line in f:
            install_requires.append(line.strip())

    return install_requires

setup(
    name='gmusic-rating-sync',
    version=gmusicSyncRatings.__version__,
    description=gmusicSyncRatings.__doc__.strip(),
    long_description=readme(),
    url='https://github.com/Bilalh/gmusic-sync-ratings',
    author=gmusicSyncRatings.__author__,
    author_email='bilalshussain@gmail.com',
    license=gmusicSyncRatings.__license__,
    packages=['gmusicSyncRatings'],
    entry_points={'console_scripts': ['gmusic-sync-rating = gmusicSyncRatings.__main__:main']},
    install_requires=requirements(),
    classifiers=[
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=['Google Music', 'Google Play', 'iTunes', 'ratings', 'music'],
    include_package_data=True,
    zip_safe=False,
)
