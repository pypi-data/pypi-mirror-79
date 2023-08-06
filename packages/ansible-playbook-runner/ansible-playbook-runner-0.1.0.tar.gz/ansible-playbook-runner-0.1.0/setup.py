#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ansible-playbook-runner',
    description='simple ansible playbook runner',
    long_description='simple ansible playbook runner',
    author='Avi Naftalis',
    author_email='anaftalis@gmail.com',
    packages=['ansible_playbook_runner'],
    install_requires='ansible>=2',
    version='0.1.0',
    setup_requires=['flake8'],
)
