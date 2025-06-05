from setuptools import setup, find_packages

setup(
    name="ra_aid_start",
    version="0.1.0",
    packages=['ra_aid_start'],
    entry_points={
        'console_scripts': [
            'ra-aid-start = ra_aid_start.__main__:main'
        ]
    }
)
