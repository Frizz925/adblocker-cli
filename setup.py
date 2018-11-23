from setuptools import setup

required = [
    'click',
    'requests',
    'six',
]

setup(
    name='AdBlocker CLI',
    version='0.1',
    packages=['adblocker'],
    author='Izra Faturrahman',
    author_email='Frizz925@hotmail.com',
    entry_points={
        'console_scripts': [
            'adblocker=adblocker.__main__:cli'
        ]
    },
    install_requires=required,
)
