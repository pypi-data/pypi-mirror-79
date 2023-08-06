from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name="easyfile-pro",
	version="0.1.0",
	keywords=["os", "tool", "file"],
	description="=======easyfile=======",
	long_description=long_description,
	license="MIT Licence",

	author="yangqi",
	author_email="geekpaul@outlook.com",

	packages=find_packages(),
	include_package_data=True,
	platforms="any",
	install_requires=[]
)
