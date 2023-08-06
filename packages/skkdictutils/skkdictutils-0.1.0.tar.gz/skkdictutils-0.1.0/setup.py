import setuptools
import re
import os

with open(os.path.join('skkdictutils', '__init__.py'), 'r', encoding='utf8') as f:
    version = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

setuptools.setup(
    name="skkdictutils",
    install_requires=['romkan>=0.2.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
    },
    entry_points={
    },
    packages=setuptools.find_packages(),
    version=version,
    license='MIT License',
    platforms=['POSIX', 'Windows', 'Unix', 'MacOS'],
    description = 'SKK dictionary utility functions',
    author='tokuhirom',
    author_email='tokuhirom@gmail.com',
    url='https://github.com/tokuhirom/skkdictutils-py',
    keywords = ['Japanese'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Natural Language :: Japanese',
        'Topic :: Text Processing',
    ],
    python_requires='>=3.6',
    long_description='%s' % (open('README.md', encoding='utf8').read()),
    test_suite = 'pytest',
)
