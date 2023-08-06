from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PappaPronta',
    author='Nicola Bernardini',
    author_email='nic.bern@tiscali.it',
    version='0.0.0',
    packages=find_packages(),
    url='https://git.smerm.org/SMERM/PappaPronta-python',
    description='PappaPronta is a library of readymade stereotyped musical objects for lazy students to produce ugly electronic music.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='stupid electronic music composition readymade stereotype dummy easy idiot',
    project_urls={
        'Source Code': 'https://git.smerm.org/SMERM/PappaPronta-python',
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    zip_safe=False,
    python_requires='>=2.7',
)
