from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read().rstrip()

setup(
    name="get_filename",
    version="1.0.0",
    keywords=("filename", "extension"),
    description="from a filename(str) extension or name",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/we684123/get_filename",
    author="we684123",
    author_email="we684123@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
