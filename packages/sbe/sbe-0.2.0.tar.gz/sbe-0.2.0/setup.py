import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="sbe",
    version="0.2.0",
    author="Chris Yuen",
    author_email="chris@kizzx2.com",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/kizzx2/sbe-python",
    install_requires=["lxml"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
