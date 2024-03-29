#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from knowledge_share/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("knowledge_share", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='django-knowledge-share',
    version=version,
    description="""App to create a microblog for sharing knowledge.""",
    long_description=readme,
    author='Vinta Software',
    author_email='contact@vinta.com.br',
    url='https://github.com/vintasoftware/django-knowledge-share',
    packages=[
        'knowledge_share',
    ],
    include_package_data=True,
    install_requires=[
        'misaka>=2.0.0,<2.2',
        'tapioca-twitter>=0.8.2,<0.9',
        'lxml>=4.5.0,<4.6.0',
        'beautifulsoup4>=4.8,<4.9',
        'pytz>=2017.2',
        'django-markdown @ git+https://github.com/vintasoftware/django_markdown@02c6fa050090b086b527de127b87f702de055dac#egg=django-markdown'
    ],
    license="MIT",
    zip_safe=False,
    keywords='django-knowledge-share',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
