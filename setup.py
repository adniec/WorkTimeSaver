from setuptools import setup
from WorkTimeSaver import __version__

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='WorkTimeSaver',
    version = __version__,
    author='Adrian Niec',
    author_email='ethru@protonmail.com',
    description='Work pretty-printer for flextime employees',
    long_description=long_description,
    url='https://github.com/ethru/WorkTimeSaver',
    license='MIT',
    platforms=['any'],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: End Users/Desktop',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Topic :: Office/Business :: Financial',
                 'Programming Language :: Python'
                 ],
    packages=['WorkTimeSaver'],
    entry_points={'console_scripts': 'WorkTimeSaver=WorkTimeSaver.__main__:main'}
)
