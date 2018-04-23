from setuptools import setup
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'README.rst'), 'r') as f:
    long_description = f.read()

with open(path.join(current_dir, 'requirements.txt'), 'r') as f:
    requirements = f.read().split('\n')

setup(
    name="autoexec",
    version="0.1.1",
    author="Felix Berkenkamp",
    author_email="fberkenkamp@gmail.com",
    description=("Automatically turn functions into executables."),
    long_description=long_description,
    url='https://github.com/befelix/autoexec',
    license="MIT",
    packages=['autoexec'],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
