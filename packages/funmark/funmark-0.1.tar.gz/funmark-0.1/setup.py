import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='funmark',  
    version='0.1',
    scripts=['funmark/Benchmark.py'] ,
    author="Jai Kumar Dewani",
    author_email="jai.dewani.99@gmail.com",
    description="A benchmarking tool for fuctions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jai-dewani/fun-mark",
    download_url="https://github.com/jai-dewani/fun-mark/archive/v_0.1.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
        "numpy", "matplotlib"
    ],
    entry_points={
        'console_scripts': ['funmark=funmar:main'],
    }
 )

'''
Run these to deploy
python setup.py sdist bdist_wheel
twine upload --repository testpypi dist/*

pip uninstall funmark
pip3 uninstall funmark
'''