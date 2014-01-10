from distutils.core import setup

_version = '2.15.0'

setup(
    name='pyPEG2',
    version=_version,
    author='Volker Birk',
    author_email='vb@dingens.org',
    packages=['pypeg2', 'pypeg2.test'],
    scripts=['samples/sample1.py', 'samples/sample2.py'],
    url='http://fdik.org/pyPEG2',
    download_url='http://fdik.org/pyPEG2/pyPEG2-' + _version + '.tar.gz',
    license='LICENSE.txt',
    description='An intrinsic PEG Parser-Interpreter for Python',
    long_description=open('README.txt').read(),
    requires=['lxml',],
    provides=['pyPEG2 (' + _version + ')',],
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
