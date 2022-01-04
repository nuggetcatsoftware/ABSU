#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ABSU',
    version='1.0',
    description='ABSU, also known as A Bunch Of Stupid Users is a discord bot aiming to user data to train a NLP set of data for chatterbot',
    long_description=open('README.md').read(),
    author='Gabs Ma',
    author_email='nuggetcatsoftware@gmail.com',
    url='https://github.com/nuggetcatsoftware/ABSU',
    packages=['chatdata'],
    install_requires=[
        'ChatterBot>=1.0.8',
        'chatterbot-corpus>=1.2.0',
        'psutil>=5.7.3',
        'discord.py==1.6.0'
    ],
    license=open('LICENSE').read()
)
