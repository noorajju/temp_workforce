#coding=utf-8
import os
from setuptools import setup, find_packages
import urllib
# Hi theere

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "workforce_optimizer",
    version = "0.0.1",
    author = "Noor",
    author_email = "noorahmedg@gmail.com",
    description = (" Work assignment optimizer"),
    long_description=read('README'),
    license = "None",
    keywords = "optimizer",
    url = "",
    packages=['workforce_optimizer', 'utils'],
    install_requires=['pulp==2.3.1','pandas==1.1.4','numpy==1.85.1'],
    entry_points = {
        'console_scripts':[
            'workforce_optimizer=workforce_optimizer.main:main',
        ],
    },
)