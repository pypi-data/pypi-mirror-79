#!/usr/bin/env python
from setuptools import setup, find_packages

with open('readme.MD') as f:
    long_description = f.read()


setup(
    name='ansible-playbook-runner',
    description='simple ansible playbook runner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Avi Naftalis',
    author_email='anaftalis@gmail.com',
    packages=['ansible_playbook_runner'],
    install_requires='ansible>=2',
    version='0.1.2',
    setup_requires=['flake8'],
    include_package_data=True,
)
