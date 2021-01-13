from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='teacup',
    url='https://github.com/MR236/TEAcup',
    author='Malcolm Risk',
    author_email='mr236@st-andrews.ac.uk',
    # Needed to actually package something
    packages=['teacup'],
    # Needed for dependencies
    install_requires=['numpy', 'pandas', 'copy', 'matplotlib'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='CC0',
    description='Python package for multi-state modelling',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.txt').read(),
)