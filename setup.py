from setuptools import setup, find_packages

setup(
    name='code2gist',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'code2gist=code2gist.main:main',
        ],
    },
)
