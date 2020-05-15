from setuptools import setup

setup(
    name='credman',
    version='1.0.0',
    py_modules=['credman'],
    install_requires=[
        'click',
        'pickledb',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        credman=credman:main
    '''
)
