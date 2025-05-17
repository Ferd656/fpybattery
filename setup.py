from setuptools import setup, find_packages

setup(
    name="fpybattery", 
    version="0.1.2",
    packages=find_packages(),
    install_requires=['torch', 'nvidia-ml-py3'],
    author="Ferd",
    author_email="ferd656@gmail.com",
    description="Ferd's battery of python functions for data science projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ferd656/fpybattery",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: Microsoft :: Windows",
    ],
    license="Unlicense",
    python_requires='>=3.11',
)
