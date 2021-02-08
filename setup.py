from setuptools import setup

setup(
    name='METER',
    url='https://github.com/MR236/METER',
    author='Malcolm Risk',
    author_email='mr236@st-andrews.ac.uk',
    packages=['METER'],
    install_requires=['numpy', 'pandas', 'matplotlib'],
    version='0.1',
    license='CC0',
    description='Python package for multi-state modelling',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
