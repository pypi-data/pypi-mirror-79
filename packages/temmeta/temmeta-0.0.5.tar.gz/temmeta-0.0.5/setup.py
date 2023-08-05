from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="temmeta",
    version="0.0.5",
    description=("TEMMETA is a library for transmission electron microscopy "
                 "(TEM) (meta)data manipulation"),
    url='https://github.com/din14970/TEMMETA',
    author='Niels Cautaerts',
    author_email='nielscautaerts@hotmail.com',
    license='GPL-3.0',
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=['Topic :: Scientific/Engineering :: Physics',
                 'Intended Audience :: Science/Research',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8'],
    keywords='TEM',
    packages=find_packages(exclude=["*tests*", "*examples*"]),
    install_requires=[
        'numpy',
        'matplotlib',
        'openpyxl',
        'pandas',
        'scipy',
        'jupyter',
        'hyperspy',
        'matplotlib_scalebar',
        'tqdm',
        'Pillow',
        'opencv-python',
    ],
)
