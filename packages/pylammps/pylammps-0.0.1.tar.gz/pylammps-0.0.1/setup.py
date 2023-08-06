#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = '2020/09/17 21:15:55'

import os
from setuptools import find_packages, setup


NAME = 'pylammps'
VERSION = '0.0.1'
DESCRIPTION = 'pylammps'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README_FILE, encoding='UTF8').read()

REQUIREMENTS = ['numpy']
URL = "https://gitee.com/alkemie_gjwang/pylammps"
AUTHOR = __author__
AUTHOR_EMAIL = __email__
LICENSE = 'MIT'
PACKAGES = find_packages()
# cmdclass = {'sdist': sdist}
PACKAGE_DATA = {}
ENTRY_POINTS = {}
# PACKAGE_DATA = {"potentialmind.data": ["fp/*.stp", "xsf/*.xsf"],
#                 "potentialmind.gui": ["generate/*.ui", "train/*.ui", "predict/*.ui", "pmlib/*.ui"]}


# # PACKAGE_DATA = {}
# ENTRY_POINTS = {
#     "gui_scripts": (
#         "pmpad = potentialmind.gui.__main__:main",
#         "pmrun = potentialmind.generate.__main__:main"
#     ),
# }


def setup_package():
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        packages=find_packages(),
        package_data=PACKAGE_DATA,
        include_package_data=True,
        entry_points=ENTRY_POINTS,
        install_requires=REQUIREMENTS,
        cmdclass={},
        zip_safe=False,
        url=URL
    )


if __name__ == '__main__':
    setup_package()
