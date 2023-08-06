#!python
#cython: language_level=3
from setuptools import find_packages,setup,Extension
import os
my_ex = Extension("vk_audio_C_FUNC",sources = ['src/C_FUNC/PyProg.cpp'],language="c++")
setup(
    name = "vk_audio",
    long_description=open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'),encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    version = "6.9",
	packages=find_packages(),
    py_modules = ["vk_api",'datetime','lxml'],
    author = "Superbespalevniy chel",
    author_email = "imartemy1@gmail.com",
    url = "https://vk.com/fesh_dragoziy",
    description = "Модуль для вызова методов аудио вк.",
    ext_modules = [my_ex],
)  