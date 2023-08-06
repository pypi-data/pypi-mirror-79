import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="messagehub",
    version="0.1.2",
    author="xinqiyang",
    author_email="xinqiyang@gmail.com",
    description="messagehub: crypto and traditional financial data hub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chaininout/messagehub",
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'requests'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
#
# NAME = 'messagehub'
# DESCRIPTION = 'messagehub project'
# URL = 'http://github.com/chaininout/messagehub'
# EMAIL = 'admin@chaininout.com'
# AUTHOR = 'xinqiyang'
# LICENSE = 'MIT'
# version = "0.1.0"
#
# pkgs = find_packages()
#
# required = [
#     'pandas',
#     'requests'
# ]
#
# s = setup(
#     name=NAME,
#     description=DESCRIPTION,
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     author=AUTHOR,
#     author_email=EMAIL,
#     url=URL,
#     version=version,
#     include_package_data=True,
#     packages=pkgs,
#     package_data={"messagehub": ["*"]},
#     install_requires=required,
#     classifiers=[
#          "Programming Language :: Python :: 3",
#          "License :: OSI Approved :: MIT License",
#          "Operating System :: OS Independent",
#      ],
# )
#
