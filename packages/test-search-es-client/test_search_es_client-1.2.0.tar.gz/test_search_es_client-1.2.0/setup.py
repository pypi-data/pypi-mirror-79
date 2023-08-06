import setuptools

with open("src/packet_name/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test_search_es_client",
    version="1.2.0",
    author="",
    author_email="",
    description="to search es client and record log",
    # 依赖包
    install_requires=[
        'aiohttp==3.6.2'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
)
