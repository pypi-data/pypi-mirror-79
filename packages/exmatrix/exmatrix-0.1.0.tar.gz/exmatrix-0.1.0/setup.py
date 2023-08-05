from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name = 'exmatrix',
    version = '0.1.0',
    description = 'A Python package to the ExMatrix method, supporting Random Forest models interpretability.',
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    url = 'https://gitlab.com/popolinneto/exmatrix',
    author = 'Mario Popolin Neto',
    license = 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International',
    classifiers = [
        'License :: Free for non-commercial use',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    package_dir = { '': 'src' },
    packages = [ 'exmatrix' ],
    python_requires = '>=3.6',
    install_requires = [ 'numpy>=1.16.0', 'matplotlib>=2.1.1', 'scikit-learn>=0.20.0', 'drawSvg>=1.6.0' ],
)