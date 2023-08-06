from setuptools import setup, find_packages

version = '0.1'
author = 'Arka Nayan'
author_email = 'hello@flowmagic.io'
description = 'FlowMagic Cli'
long_description = description

install_requires = [
    'click>=7.1.2',
    'requests>=2.24.0'
]

setup(
    name='flowmagic-cli',
    version=version,
    description=description,
    long_description=long_description,
    url='https://flowmagic.io/',
    author=author,
    author_email=author_email,
    packages=find_packages(),
    package_data={'cli': ['data/.gitignore', 'data/config.json', 'data/Dockerfile']},
    entry_points={
        'console_scripts': [
            'flowmagic = cli.__init__:flowmagic',
        ],
    },
    python_requires='>=3.6',
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)