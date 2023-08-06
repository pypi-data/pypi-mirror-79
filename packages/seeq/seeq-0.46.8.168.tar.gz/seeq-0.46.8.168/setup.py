import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seeq",
    version="0.46.08.168",
    author="Seeq Corporation",
    author_email="support@seeq.com",
    description="The Seeq SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.seeq.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'certifi',
        'ipython>=7.6.1',
        'matplotlib>=3.1.1',
        'numpy>=1.16.4',
        'pandas>=0.24.2',
        'beautifulsoup4>=4.8.0',
        'Deprecated>=1.2.6',
        'Mako>=1.1.0',
        'six',
        'urllib3',
        'requests',
        'ipywidgets>=7.5.1',
        'tzlocal>=2.0.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
