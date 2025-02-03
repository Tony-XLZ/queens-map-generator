from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    name="solver_cy",
    ext_modules=cythonize("solver_cy.pyx", compiler_directives={'language_level': "3"}),
    include_dirs=[np.get_include()]
)
