from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        name="generator_cy",
        sources=["generator_cy.pyx"],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        name="solver_cy",
        sources=["solver_cy.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    name="MyProject",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)
