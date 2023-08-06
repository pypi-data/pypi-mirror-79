#encoding:utf-8
import shutil
import os
from setuptools import setup, Extension
module = Extension("{{ module_name }}", sources=["{{ module_name }}.{{ module_type }}"])
setup(ext_modules=[module],script_args=["build_ext",'-i',"clean","--all"])