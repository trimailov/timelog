from setuptools import setup

setup(
    name='timeflow',
    version='0.1',
    py_modules=['timeflow'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        timeflow=timeflow:cli
    ''',
)
