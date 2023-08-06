import setuptools
import os
import sys

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'requests==2.24.0'
]

setuptools.setup(
    name="reqtry",
    version="0.0.2",
    author="Marco Urriola",
    author_email="marco.urriola@gmail.com",
    description="A simple implementation of retries for request Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marc0u/reqtry",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requires,
)
