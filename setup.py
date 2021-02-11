from setuptools import setup

setup(
    name='METER',
    url='https://github.com/MR236/METER',
    author='Malcolm Risk',
    author_email='mr236@st-andrews.ac.uk',
    packages=['METER'],
    install_requires=['numpy', 'pandas', 'matplotlib'],
    version='0.5.5',
    license='CC0',
    description='Multi-state Estimates for Time-to-Event Research',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={'Documentation': 'https://meter1.readthedocs.io/en/latest/'}
)
