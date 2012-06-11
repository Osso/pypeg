from distutils.core import setup

setup(
    name='pyPEG2',
    version='2.5.3',
    author='Volker Birk',
    author_email='vb@dingens.org',
    packages=['pypeg2', 'pypeg2.test'],
    scripts=['samples/sample1.py', 'samples/sample2.py'],
    url='http://fdik.org/pyPEG2',
    download_url='http://fdik.org/pyPEG2/pyPEG2.tar.gz',
    license='LICENSE.txt',
    description='An intrinsic PEG Parser-Interpreter for Python',
    long_description=open('README.txt').read(),
    requires=['lxml',],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
