from setuptools import setup, find_packages
import scrim

with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name=scrim.__title__,
    version=scrim.__version__,
    url=scrim.__url__,
    license=scrim.__license__,
    author=scrim.__author__,
    author_email=scrim.__email__,
    description=scrim.__description__,
    long_description=long_description,
    install_requires=[
        'click>=6.7',
        'psutil>=5.2',
    ],
    packages=['scrim'],
    package_data={
        'scrim': ['bin/*.*']
    },
    entry_points={
        'console_scripts': [
            'scrim = scrim.__main__:cli'
        ]
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
