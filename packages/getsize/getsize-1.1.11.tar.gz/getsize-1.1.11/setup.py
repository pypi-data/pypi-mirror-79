# Copyright (c) 2019 Sergey Barskov
# This code is licensed under MIT License (see LICENSE for details)

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='getsize',
    version='1.1.11',
    description='Get and display the size of file and directory with binary prefixes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sergey Barskov',
    author_email='sergeybarskov@gmail.com',
    url='https://github.com/JeXLiN/getsize',
    license='MIT',
    py_modules=['getsize'],
    entry_points={'console_scripts': ['getsize = getsize:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
