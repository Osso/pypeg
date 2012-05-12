from distutils.core import setup

setup(
    name='pyPEG',
    version='2.0.0',
    author='Volker Birk',
    author_email='vb@dingens.org',
    packages=['pypeg2', 'pypeg2.xmlast2', 'pypeg2.test'],
    scripts=[],
    url='http://fdik.org/pyPEG',
    license='LICENSE.txt',
    description='A PEG Parser-Interpreter in Python',
    long_description=open('README.txt').read(),
    install_requires=[],
)
