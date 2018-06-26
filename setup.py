from setuptools import setup

setup(
    name='numpy-turtle',
    version='0.1',
    packages=['numpy_turtle'],
    python_requires='>=3.5',
    install_requires=['numpy>=1.13.1', 'scikit_image>=0.13.1'],
    url='https://github.com/jorenham/numpy_turtle',
    license='MIT',
    author='Joren Hammudoglu',
    author_email='joren@bootbootboot.nl',
    description='Turtle graphics with NumPy',
    test_suite='nose.collector',
    tests_require=['nose', 'tox'],
)
