from setuptools import setup

setup(
    name='teacup',
    url='https://github.com/MR236/TEAcup',
    author='Malcolm Risk',
    author_email='mr236@st-andrews.ac.uk',
    packages=['teacup'],
    install_requires=['numpy', 'pandas', 'copy', 'matplotlib'],
    version='0.1',
    license='CC0',
    description='Python package for multi-state modelling',
    long_description=open('README.txt').read(),
)
