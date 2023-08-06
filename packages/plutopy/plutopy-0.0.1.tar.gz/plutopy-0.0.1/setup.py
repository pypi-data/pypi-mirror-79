import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plutopy",
    version="0.0.1",
    author="WardenAllen",
    author_email="908824040@qq.com",
    description="WardenAllen's Library Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/WardenAllen",
    packages=setuptools.find_packages(),
    install_requires=[
        'xlrd',
        'toml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)