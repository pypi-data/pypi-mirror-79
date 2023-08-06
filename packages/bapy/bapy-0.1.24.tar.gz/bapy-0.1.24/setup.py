#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

from bapy import path, ic, ask, console, Url, User, asdict

ic(path.scripts_relative)
ic(path.scripts)
ic(type(path.scripts))

post = True


def post_command(obj):
    """
    Post Install Command.

    Args:
        obj: post command self obj.
    """
    ic(asdict(obj))
    if post and not obj.root.startswith('build/bdist.macosx'):
        if ask('Do you want to?'):
            console.print("Start installation!")
    return obj


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    function = post_command
    # Pre Install.

    def run(self):
        # Post Install.
        if self.function:
            # noinspection PyArgumentList
            self.function()
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    function = post_command
    # Pre Install.

    def run(self):
        # Post Install.
        if self.function:
            # noinspection PyArgumentList
            self.function()
        install.run(self)


PostDevelopCommand.function = PostInstallCommand.function = post_command


setup(
    author=User.gecos,
    author_email=Url.email(User.name),
    cmdclass={
        'develop': PostDevelopCommand,
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
    package_data={
        'path.repo': [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
    },
    packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires='>=3.8,<4',
    scripts=[item.text for item in path.scripts],
    setup_requires=path.project.requirements['requirements_setup'],
    tests_require=path.project.requirements['requirements_test'],
    url=Url.lumenbiomics(http=True, repo=path.repo).url,
    use_scm_version=False,
    version='0.1.24',
    zip_safe=False,
)

# def post_command(obj):
#     """
#     Post Install Command.
#
#     Args:
#         obj: post command self obj.
#     """
#     def post_actions():
#         ic(obj)
#         if post:
#             if ask('Do you want to?'):
#                 console.print("Start installation!")
#     post_actions()
#     return obj
#
# setup = post_command(
#     setup(
#         author=User.gecos,
#         author_email=Url.email(User.name),
#         description=path.project.description(),
#         entry_points={
#             'console_scripts': [
#                 f'{path.repo} = {path.repo}:app',
#             ],
#         },
#         install_requires=path.project.requirements['requirements'],
#         name=path.repo,
#         packages=find_packages(include=[path.repo], exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
#         python_requires='>=3.8,<4',
#         scripts=path.scripts_relative,
#         setup_requires=path.project.requirements['requirements_setup'],
#         tests_require=path.project.requirements['requirements_test'],
#         url=Url.lumenbiomics(http=True, repo=path.repo).url,
#         use_scm_version=False,
#         version='0.1.24',
#         zip_safe=False,
#     )
# )
