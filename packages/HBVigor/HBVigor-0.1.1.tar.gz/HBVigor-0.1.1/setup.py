from __future__ import print_function
from setuptools import setup, find_packages
import sys
# Get long description in READ.md file
with open("README.md", "r",encoding='utf-8') as fh:
    LONG_DESCRIPTION = fh.read()


setup(
    name="HBVigor",
    version="0.1.1",
    author="fengzhizi",
    author_email="fengzhizi32@live.com",
    description="HBV.",
    license="MIT",
    url="",  # github地址或其他地址
    packages=find_packages(),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

    ],
    install_requires=[
        "scipy",  # 所需要包的版本号
        "numpy",  # 所需要包的版本号
        #"math",  # 所需要包的版本号
        "astropy",
    ],
    zip_safe=True,
)