from setuptools import setup, find_packages
from Cython.Build import cythonize
import numpy

setup(
    name='maze',
    packages=find_packages(),
    ext_modules=cythonize('maze/solver.pyx', language_level=3, include_dirs=[numpy.get_include()]),
    include_dirs=[numpy.get_include()],
    install_requires=[
        'Cython',
        'NumPy',
    ],
)