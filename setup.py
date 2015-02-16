import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='python-zimbra',
    version='2.0',
    packages=['pythonzimbra'],
    include_package_data=True,
    license='BSD 2-clause License',  # example license
    description='Python classes to access Zimbra SOAP backend with a few utilities.',
    long_description=README,
    url='https://github.com/Zimbra-Community/python-zimbra',
    author='Dennis Ploeger',
    author_email='develop@dieploegers.de',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries'
    ],
)
