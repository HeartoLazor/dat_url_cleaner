import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    entry_points={
        'console_scripts': [
            'dat_url_cleaner = dat_url_cleaner.dat_url_cleaner:main'
        ]
    },
    name="dat_url_cleaner",
    include_package_data=True,
    version="1.0.0",
    author="Hearto Lazor",
    author_email="heartolazor@gmail.com",
    description="Clean a list of urls using a Rom management Dat file",
    keywords ="Romset organization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HeartoLazor/dat_url_cleaner",
    install_requires=[],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    )
)