from setuptools import setup, find_packages

_version = '2.15.0'

setup(
    name='pyPEG2',
    version=_version,
    author='Volker Birk',
    author_email='vb@dingens.org',
    packages=find_packages(),
    url='http://fdik.org/pyPEG2',
    download_url='http://fdik.org/pyPEG2/pyPEG2-' + _version + '.tar.gz',
    license='LICENSE.txt',
    description='An intrinsic PEG Parser-Interpreter for Python',
    long_description=open('README.md').read(),
    requires=['lxml', 'ordereddict'],
    provides=['pyPEG2 (' + _version + ')'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
