from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setup(
    name="CaMo",
    version="0.0.3",
    author="Alessio Zanga",
    author_email="alessio.zanga@outlook.it",
    license="GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007",
    description="CaMo: A Causal Model Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
       "Development Status :: 1 - Planning",
       "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms=[
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS",
    ],
    url="https://github.com/AlessioZanga/CaMo",
    packages=find_packages(),
    include_package_data=True,
    package_data={"camo": ["data/*.gz"]},
    install_requires=requirements,
)
