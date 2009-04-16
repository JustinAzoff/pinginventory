from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='pinginventory',
    version=version,
    description="Inventory devices using ICMP",
    long_description=""" """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='ICMP scan',
    author='Justin Azoff',
    author_email='JAzoff@uamail.albany.edu',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points={
        'console_scripts':[
            'pinginventory-take-inventory = pinginventory.commands:take_inventory',
            'pinginventory-show-ip = pinginventory.commands:show_ip',
        ]
    }
)
