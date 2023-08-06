import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='iosolver',
    version='0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/jackl001/iosolver',
    license='MIT',
    author='jackl001',
    author_email='caozhankui@outlook.com',
    description='A package used for io operations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)