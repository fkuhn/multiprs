import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'pyyaml', 'lxml', 'pytest'
    ]
setup(
    name="multiprs",
    version="0.3",
    author="Florian Kuhn",
    author_email = "kuhn@ids-mannheim.de",
    description = ("tagging and metadata alignment for multilit"),
    license = "MIT",
    keywords = "tagging parsing corpus",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=find_packages('src'),
    package_dir = {'': 'src'}, include_package_data=True,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['multiprs=multiprs:main']
    }
)
