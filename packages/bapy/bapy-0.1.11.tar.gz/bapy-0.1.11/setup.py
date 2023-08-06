#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
import setuptools

from bapy import path, postcommand, PostDevelopCommand, PostInstallCommand, Url, User

PostDevelopCommand.function = PostInstallCommand.function = postcommand

setuptools.setup(
    author=User.gecos,
    author_email=Url.email(User.user),
    cmdclass={
        # 'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    description=path.project.description(),
    entry_points={
        'console_scripts': [
            f'{path.repo} = {path.repo}:app',
        ],
    },
    install_requires=path.project.requirements['requirements'],
    name=path.repo,
    packages=setuptools.find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires='>=3.8,<4',
    scripts=path.scripts_relative,
    setup_requires=path.project.requirements['requirements_setup'],
    tests_require=path.project.requirements['requirements_test'],
    use_scm_version=False,
    version='0.1.11',
    zip_safe=False,
)
