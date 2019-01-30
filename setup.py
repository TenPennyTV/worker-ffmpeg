"""A simple hash function with issues"""

import tenpenny_ffmpeg

from setuptools import setup, find_packages


def readfile(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


setup(
    name=tenpenny_ffmpeg.__title__,
    version=tenpenny_ffmpeg.__version__,
    license=tenpenny_ffmpeg.__license__,
    author=tenpenny_ffmpeg.__author__,
    url='',
    author_email='jimmy@tenpenny.tv',
    description=__doc__,
    long_description='\n\n'.join(map(readfile, ('README.md',))),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        #  As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Internet',
    ],
    test_suite="tests"
)